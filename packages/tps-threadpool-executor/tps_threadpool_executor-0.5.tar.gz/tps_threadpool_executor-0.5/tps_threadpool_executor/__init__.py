import json
import time
from queue import Queue
import threading
from threadpool_executor_shrink_able.sharp_threadpoolexecutor import ThreadPoolExecutorShrinkAble
import nb_log
import redis
import decorator_libs
import socket
import os

"""
这个线程池和一般线程池不同，是自动控频的，能够将任意函数控制成指定的运行频率。
此线程池入参不是设置并发大小，而是设置tps大小。

TpsThreadpoolExecutor 基于单进程的当前线程池控频。
DistributedTpsThreadpoolExecutor 基于多台机器的分布式控频，需要安装redis，统计出活跃线程池，从而平分任务。

比如要吧服务端压测 10000 tps每秒，python单进程 + 多线程 requests urllib3 没办法做到500tps，
此时可以使用 DistributedTpsThreadpoolExecutor，多进程 + 多台机器 会非常精确的对服务端产生 10000 qps的压力。
"""


class TpsThreadpoolExecutor:
    def __init__(self, tps=0):
        """
        :param tps:   指定线程池每秒运行多少次函数，为0这不限制运行次数
        """
        self.tps = tps
        self.time_interval = 1 / tps if tps != 0 else 0
        self.pool = ThreadPoolExecutorShrinkAble(500)  # 这是使用的智能线程池，所以可以写很大的数字，具体见另一个包的解释。
        self.queue = Queue(500)
        threading.Thread(target=self._put_task_to_pool_queue).start()

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
        self._pool_identify =pool_identify
        super(DistributedTpsThreadpoolExecutor, self).__init__(tps=tps)
        self.redis_db = redis.from_url(redis_url)
        self.redis_key_pool_identify = f'DistributedTpsThreadpoolExecutor:{pool_identify}'
        ip, host_name = get_host_ip()
        self.current_process_flag = f'{ip}-{host_name}-{os.getpid()}-{id(self)}'
        self._send_heartbeat_to_redis()
        self._last_show_pool_instance_num = time.time()

    @decorator_libs.keep_circulating(10, block=False, daemon=True)
    def _send_heartbeat_to_redis(self):
        all_identify = self.redis_db.smembers(self.redis_key_pool_identify)
        pool_instance_num = len(all_identify)
        if time.time() - self._last_show_pool_instance_num > 60:
            self.logger.debug(f'分布式环境中一共有 {pool_instance_num} 个  {self._pool_identify} 标识的线程池')
        self.time_interval = (1.0 / self.tps) * pool_instance_num if self.tps != 0 else 0
        for identify in all_identify:
            identify_dict = json.loads(identify)
            if identify_dict['current_process_flag'] == self.current_process_flag:
                self.redis_db.srem(self.redis_key_pool_identify, identify)
            if time.time() - identify_dict['last_heartbeat_ts'] > 15:
                self.redis_db.srem(self.redis_key_pool_identify, identify)
        self.redis_db.sadd(self.redis_key_pool_identify, json.dumps(
            {'current_process_flag': self.current_process_flag, 'last_heartbeat_ts': time.time(), 'last_heartbeat_time_str': time.strftime('%Y-%m-%d %H:%M:%S')}))


if __name__ == '__main__':
    def f1(x):
        time.sleep(0.1)
        print(x)


    def f2(x):
        time.sleep(3)
        print(x)


    # tps_pool = TpsThreadpoolExecutor(tps=7)  # 这个是单机控频
    tps_pool = DistributedTpsThreadpoolExecutor(tps=7, pool_identify='pool_for_use_print')  # 这个是redis分布式控频，不是基于incr计数的，是基于
    for i in range(10000):
        tps_pool.submit(f1, i)
        tps_pool.submit(f1, i * 10)
