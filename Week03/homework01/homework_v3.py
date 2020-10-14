# -*- coding: utf-8 -*-
"""
@author : Yx
"""

# # 示例代码
# import threading
# class DiningPhilosophers:
#    def __init__(self):
#    pass
# # philosopher 哲学家的编号。
# # pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
# # eat 表示吃面。
# # putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
#    def wantsToEat(self,
#       philosopher,
#       pickLeftFork(),
#       pickRightFork(),
#       eat(),
#       putLeftFork(),
#       putRightFork())
# 参考waiter模式，

import queue
import threading
import time
import random


class DiningPhilosopher(threading.Thread):
    def __init__(self, philosopher, fork_locks, fork_status, q, eat_times=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.philosopher_num = philosopher
        # self.philosopher_name = f'哲学家{philosopher}'
        self.fork_locks = fork_locks
        self.fork_status = fork_status
        self.q = q
        self.eat_times = eat_times
        self.left_fork_num = self.philosopher_num % len(fork_locks)
        self.right_fork_num = (self.philosopher_num + 1) % len(fork_locks)

    def wantsToEat(self, *actions):
        [action() for action in actions]

    def run(self):
        current_time = 1
        self.think()
        while current_time <= self.eat_times:
            # 如果同时举起左侧Fork (0,0),(1,1),(2,2),(3,3),(4,4) -> 产生死锁
            # 判断左右叉子状态后，决定是否吃
            if not self.fork_status[self.left_fork_num] and not self.fork_status[self.right_fork_num]:
                self.wantsToEat(
                    self._pickLeftFork,
                    self._pickRightFork,
                    self._eat,
                    self._putLeftFork,
                    self._putRightFork
                )
                current_time += 1
            self.think()

    def think(self):
        think_time = random.randint(1, 5) / 100
        time.sleep(think_time)

    def _pickLeftFork(self):
        self.fork_status[self.left_fork_num] = True
        self.fork_locks[self.left_fork_num].acquire()
        self.q.put([self.philosopher_num, 1, 1])

    def _pickRightFork(self):
        self.fork_status[self.right_fork_num] = True
        self.fork_locks[self.right_fork_num].acquire()
        self.q.put([self.philosopher_num, 2, 1])

    def _eat(self):
        eat_time = random.randint(1, 3) / 100
        time.sleep(eat_time)
        self.q.put([self.philosopher_num, 0, 3])
        print(f'philosopher {self.philosopher_num} eat noodle')

    def _putLeftFork(self):
        self.fork_locks[self.left_fork_num].release()
        self.fork_status[self.left_fork_num] = False
        self.q.put([self.philosopher_num, 1, 2])

    def _putRightFork(self):
        self.fork_locks[self.right_fork_num].release()
        self.fork_status[self.right_fork_num] = False
        self.q.put([self.philosopher_num, 2, 2])


def main(philosopher_num):
    threads = []
    fork_locks = []
    result = []
    q = queue.Queue()
    for i in range(philosopher_num):
        fork_lock = threading.Lock()
        fork_locks.append(fork_lock)
    eat_times = 5

    fork_status = [False] * len(fork_locks)

    for i in range(philosopher_num):
        t = DiningPhilosopher(i, q=q, fork_locks=fork_locks, fork_status=fork_status, eat_times=eat_times)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    while not q.empty():
        result.append(q.get())

    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(str(result) + '\n')


if __name__ == '__main__':
    main(5)
