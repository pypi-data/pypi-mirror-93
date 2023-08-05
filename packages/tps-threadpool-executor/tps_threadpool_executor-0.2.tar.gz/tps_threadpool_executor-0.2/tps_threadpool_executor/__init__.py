import time
from queue import Queue
import threading
from threadpool_executor_shrink_able.sharp_threadpoolexecutor import ThreadPoolExecutorShrinkAble

"""
这个线程池和一般线程池不同，是自动控频的，能够将任意函数控制成指定的运行频率。
此线程池入参不是设置并发大小，而是设置tps大小。
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


if __name__ == '__main__':
    def f1(x):
        time.sleep(0.1)
        print(x)


    def f2(x):
        time.sleep(3)
        print(x)


    tps_pool = TpsThreadpoolExecutor(tps=7)
    for i in range(1000):
        tps_pool.submit(f1, i)
        tps_pool.submit(f1, i * 10)
