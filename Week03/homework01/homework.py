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
import queue
import threading
import time
import random


class DiningPhilosopher(threading.Thread):
    def __init__(self, philosopher, fork_locks, q, eat_times=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.philosopher_num = philosopher
        self.philosopher_name = f'哲学家{philosopher}'
        self.fork_locks = fork_locks
        self.q = q
        self.eat_times = eat_times
        self.left_fork_num = self.philosopher_num % 5
        self.right_fork_num = (self.philosopher_num + 1) % 5

    def wantsToEat(self, *actions):
        [action() for action in actions]

    def run(self):
        current_time = 1
        self.think()
        while current_time <= self.eat_times:
            self.wantsToEat(
                self._pickLeftFork,
                self._pickRightFork,
                self._eat,
                self._putLeftFork,
                self._putRightFork
            )
            current_time += 1

    def think(self):
        think_time = random.randint(1, 5) / 10
        time.sleep(think_time)

    def _pickLeftFork(self):
        self.fork_locks[self.left_fork_num].acquire()
        self.q.put([self.philosopher_num, self.left_fork_num, 1])
        print(f'{self.philosopher_name} pickLeftFork')

    def _pickRightFork(self):
        self.fork_locks[self.right_fork_num].acquire()
        self.q.put([self.philosopher_num, self.right_fork_num, 1])
        print(f'{self.philosopher_name} pickRightFork')

    def _eat(self):
        eat_time = random.randint(1, 3) / 10
        time.sleep(eat_time)
        self.q.put([self.philosopher_num, 0, 3])
        print(f'{self.philosopher_name} eat noodle')

    def _putLeftFork(self):
        self.fork_locks[self.left_fork_num].release()
        self.q.put([self.philosopher_num, self.left_fork_num, 2])
        print(f'{self.philosopher_name} putLeftFork')

    def _putRightFork(self):
        self.fork_locks[self.right_fork_num].release()
        self.q.put([self.philosopher_num, self.right_fork_num, 2])
        print(f'{self.philosopher_name} putRightFork')


def main():
    threads = []
    fork_locks = []
    result = []
    q = queue.Queue()
    for i in range(5):
        fork_lock = threading.Lock()
        fork_locks.append(fork_lock)
    eat_times = 5

    for i in range(5):
        t = DiningPhilosopher(i, q=q, fork_locks=fork_locks, eat_times=eat_times)
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
    main()
