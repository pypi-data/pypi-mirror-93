import json
import time
from queue import Queue, Empty
import threading
from threadpool_executor_shrink_able.sharp_threadpoolexecutor import ThreadPoolExecutorShrinkAble
import nb_log
import redis
import decorator_libs
import socket
import os
import multiprocessing
import atexit

"""
这个线程池和一般线程池不同，是自动控频的，能够将任意函数控制成指定的运行频率。
此线程池入参不是设置并发大小，而是设置tps大小。

TpsThreadpoolExecutor 基于单进程的当前线程池控频。
DistributedTpsThreadpoolExecutor 基于多台机器的分布式控频，需要安装redis，统计出活跃线程池，从而平分任务。

比如要吧服务端压测 10000 tps每秒，python单进程 + 多线程 requests urllib3 没办法做到500tps，
此时可以使用 DistributedTpsThreadpoolExecutor，多进程 + 多台机器 会非常精确的对服务端产生 10000 qps的压力。
"""


class TpsThreadpoolExecutor(nb_log.LoggerMixin):
    put_task_to_pool_queue_thread_daemon = True

    def __init__(self, tps=0):
        """
        :param tps:   指定线程池每秒运行多少次函数，为0这不限制运行次数
        """
        self.tps = tps
        self.time_interval = 1 / tps if tps != 0 else 0
        self.pool = ThreadPoolExecutorShrinkAble(500)  # 这是使用的智能线程池，所以可以写很大的数字，具体见另一个包的解释。
        self.queue = Queue(500)
        threading.Thread(target=self._put_task_to_pool_queue, daemon=self.put_task_to_pool_queue_thread_daemon).start()  # 这里是守护，不然程序无法结束。
        atexit.register(self._at_exit)

    def _at_exit(self):
        while True:
            time.sleep(self.time_interval)
            try:
                task = self.queue.get(block=False)
                self.pool.submit(task[0], *task[1], **task[2])
            except Exception:  # 两种Empty
                self.logger.info('真的要结束了')
                break

    def submit(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def _put_task_to_pool_queue(self):
        while True:
            time.sleep(self.time_interval)
            task = self.queue.get()
            self.pool.submit(task[0], *task[1], **task[2])

    def shutdown(self, wait=True):
        self.pool.shutdown(wait=wait)


def get_host_ip():
    ip = ''
    host_name = ''
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.connect(('8.8.8.8', 80))
        ip = sc.getsockname()[0]
        host_name = socket.gethostname()
        sc.close()
    except Exception:
        pass
    return ip, host_name


class DistributedTpsThreadpoolExecutor(TpsThreadpoolExecutor, nb_log.LoggerMixin):
    """
    这个是redis分布式控频线程池，不是基于incr计数的，是基于统计活跃消费者，然后每个线程池平分频率的。
    """

    def __init__(self, tps=0, pool_identify: str = None, redis_url: str = 'redis://:@127.0.0.1/0'):
        """
        :param tps: 指定线程池每秒运行多少次函数，为0这不限制运行次数
        :param pool_identify: 对相同标识的pool，进行分布式控频,例如多台机器都有标识为1的线程池，则所有机器加起来的运行次数控制成指定频率。
        :param redis_url:   'redis://:secret@100.22.233.110/7'
        """
        if pool_identify is None or redis_url is None:
            raise ValueError('设置的参数错误')
        self._pool_identify = pool_identify
        super(DistributedTpsThreadpoolExecutor, self).__init__(tps=tps)
        # self.queue = multiprocessing.Queue(500)
        self.redis_db = redis.from_url(redis_url)
        self.redis_key_pool_identify = f'DistributedTpsThreadpoolExecutor:{pool_identify}'
        ip, host_name = get_host_ip()
        self.current_process_flag = f'{ip}-{host_name}-{os.getpid()}-{id(self)}'
        self._heartbeat_interval = 10
        decorator_libs.keep_circulating(self._heartbeat_interval, block=False, daemon=True)(self._send_heartbeat_to_redis)
        threading.Thread(target=self._run__send_heartbeat_to_redis_2_times).start()
        self._last_show_pool_instance_num = time.time()

    def _run__send_heartbeat_to_redis_2_times(self):
        """ 使开始时候快速检测两次"""
        self._send_heartbeat_to_redis()
        time.sleep(2)
        self._send_heartbeat_to_redis()

    def _send_heartbeat_to_redis(self):
        all_identify = self.redis_db.smembers(self.redis_key_pool_identify)
        for identify in all_identify:
            identify_dict = json.loads(identify)
            if identify_dict['current_process_flag'] == self.current_process_flag:
                self.redis_db.srem(self.redis_key_pool_identify, identify)
            if time.time() - identify_dict['last_heartbeat_ts'] > self._heartbeat_interval + 1:
                self.redis_db.srem(self.redis_key_pool_identify, identify)
        self.redis_db.sadd(self.redis_key_pool_identify, json.dumps(
            {'current_process_flag': self.current_process_flag, 'last_heartbeat_ts': time.time(), 'last_heartbeat_time_str': time.strftime('%Y-%m-%d %H:%M:%S')}))
        pool_instance_num = self.redis_db.scard(self.redis_key_pool_identify)
        if time.time() - self._last_show_pool_instance_num > 60:
            self.logger.debug(f'分布式环境中一共有 {pool_instance_num} 个  {self._pool_identify} 标识的线程池')
        self.time_interval = (1.0 / self.tps) * pool_instance_num if self.tps != 0 else 0


class DistributedTpsThreadpoolExecutorUseProcessQueue(DistributedTpsThreadpoolExecutor):
    put_task_to_pool_queue_thread_daemon = False

    def __init__(self, tps=0, pool_identify: str = None, redis_url: str = 'redis://:@127.0.0.1/0', queue: multiprocessing.Queue = None):
        super().__init__(tps, pool_identify, redis_url)
        self.queue = queue


class DistributedTpsThreadpoolExecutorWithMultiProcess:
    """ 自动开多进程 + 线程池的方式。 例如你有一台128核的压测机器 对 web服务端进行压测，要求每秒压测1万 tps，单进程远远无法做到，可以方便设置 process_num 为 100"""
    """ 部分场景使用方式下只支持linux，原因自己百度多进程之linux的fork和win的spwan,同样的代码多进程在linux和win表现区别很大（包括pickle序列化 和 if name == __main__）"""

    def _start_a_threadpool(self, ):
        DistributedTpsThreadpoolExecutorUseProcessQueue(self.tps, self._pool_identify, self.redis_url, self.queue)

    def __init__(self, tps=0, pool_identify: str = None, redis_url: str = 'redis://:@127.0.0.1/0', process_num=1):
        self.queue = multiprocessing.Queue(500)
        self.tps = tps
        self._pool_identify = pool_identify
        self.redis_url = redis_url
        for _ in range(process_num):
            multiprocessing.Process(target=self._start_a_threadpool, ).start()

    def submit(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def shutdown(self, wait=True):
        pass


def f1(x):
    time.sleep(0.1)
    print(x)


def f2(x):
    time.sleep(3)
    print(x)


if __name__ == '__main__':
    # tps_pool = TpsThreadpoolExecutor(tps=7)  # 这个是单机控频
    # tps_pool = DistributedTpsThreadpoolExecutor(tps=7, pool_identify='pool_for_use_print')  # 这个是redis分布式控频，不是基于频繁incr计数的，是基消费者数量统计的。
    tps_pool = DistributedTpsThreadpoolExecutorWithMultiProcess(tps=10, pool_identify='pool_for_use_print', process_num=5)  # 这个是redis分布式控频，不是基于incr计数的，是基于
    for i in range(1000):
        tps_pool.submit(f1, i)
        tps_pool.submit(f1, i * 10)
