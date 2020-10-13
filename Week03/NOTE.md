学习笔记

## 多进程
### 多进程父子关系和进程创建
进程之间创建的进程叫做子进程
创建进程的两种方式
- os.fork()
- multiprocessing.Process()
#### multiprocessing.Process创建子进程
```python
from multiprocessing import Process
def fun(name):
    print(f'hello {name}')

p = Process(target=fun,args=('Tom',))
p.start()
# 父进程等待子进程结束后再结束,[timeout]阻塞 timeout秒
# 若超时 join()返回 None,判断None来确定是否超时
p.join(5)
```
#### Process对象属性及其他方法
```python
import multiprocessing
from multiprocessing import Process
def f(name):
    print(name)
p = Process(target=f, name='p-1', args=('bob',))
# 两个属性pid,name
print(p.pid,p.name)
# 方法
p.start(),p.join(),p.terminate()
# 获取活动的子进程
print(multiprocessing.active_children())
# 获取核心数量
print(multiprocessing.cpu_count())

```
#### 通过类的继承创建子进程
自定义类继承自Process类，通过重写run()方法实现进程的任务
```python
import os
import time
from multiprocessing import Process


class NewProcess(Process):
    def __init__(self,num):
        self.num = num
        super().__init__()

    def run(self):
        while True:
            print(f'我是进程 {self.num} ,我的pid 是{os.getpid()}')
            time.sleep(1)

# 注：有子进程必须保证程序中存在main函数
if __name__ == '__main__':
    for i in range(2):
        p = NewProcess(i)
        p.start()
```
### 进程通信
#### 进程之间变量不能共享
每个进程（父进程、子进程）变量都存在自己的堆栈中相互之间不能共享
#### 队列 Queue
多进程、多线程比较推荐的一个通信方式，队列是进程安全的
##### Queue主要方法
- put(block=True,timeout=None)
  - 如果block为True，则为阻塞队列，队列满时会等待timeout的时间，然后抛出_queue.Full异常
  - 如果block为False，则为非阻塞队列，队列满时不等待，直接抛出_queue.Empty异常
- get(block=True,timeout=None)
  - 如果block为True，则为阻塞队列，队列空时会等待timeout的时间，然后抛出_queue.Empty异常
  - 如果block为False，则为非阻塞队列，队列空时不等待，直接抛出_queue.Empty异常   
#### 管道 Pipe（不推荐）
进程不安全，同时发送或接收有可能导致数据损坏
```python
from multiprocessing import Process, Pipe

def f(conn):
    # 子进程发送
    conn.send([42,None,'hello'])
    conn.close()

if __name__ == '__main__':
    #创建管道两端
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    # 父进程接收
    print(parent_conn.recv())
    p.join()
```
#### 共享内存
```python
from multiprocessing import Process, Value, Array


def f(n, a):
    # Value.value赋值
    n.value = 3.1415927
    for i in a:
        a[i] = -a[i]


if __name__ == '__main__':
    # 定义变量类型double
    num = Value('d', 0.0)
    # 定义变量类型Array(int)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```
#### 进程锁
在使用共享内存时，需要在进程内加锁，使用完成后释放锁
```python
import multiprocessing as mp
import time


def job(v, num, l):
    # 加锁
    l.acquire()
    for _ in range(5):
        time.sleep(0.1)
        v.value += num
        print(v.value, end="|")
    # 释放
    l.release()

if __name__ == '__main__':
    def main():
        l = mp.Lock()
        v = mp.Value('i', 0)
        p1 = mp.Process(target=job, args=(v, 1, l))
        p2 = mp.Process(target=job, args=(v, 3, l))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

```
### 进程池
#### 创建进程池
```python
import multiprocessing
from multiprocessing.pool import Pool

def f(name):
    print(name)

if __name__ == '__main__':
    num = multiprocessing.cpu_count()
    p = Pool(num)
    for i in range(24):
        # 异步执行
        p.apply_async(f,args=(f'tom{i}',))
    # close等待进程完成后结束
    p.close()
    # join等待所有子进程结束父进程再结束
    p.join()
    # terminate强制进程结束
    p.terminate()
```
#### 防止死锁
- 使用队列后，在join后不能再取队列数据
- 进程池的join需要再close或terminate方法之后
#### 创建进程池(with)
```python
import multiprocessing
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    num = multiprocessing.cpu_count()
    with Pool(processes=num) as pool:
        # 有返回值时，接收后用get()获取 
        result = pool.apply_async(f,(10,))
        # 超时后，抛出异常TimeoutError
        print(result.get(timeout=1))
```
#### 使用map函数创建进程
```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        # 只能接收一个参数，多个参数需要打包处理
        print(pool.map(f, range(10))) 
        # 输出迭代器
        it = pool.imap(f, range(10))  
        print(it)               
        print(next(it))               
        print(next(it))               
        print(it.next(timeout=1))     
```

## 多线程
### 阻塞非阻塞，同步异步
- 阻塞非阻塞针对于发起方，调用方，阻塞为等待不能做别的事情，非阻塞为不等待可以做别的事情
- 同步异步针对于被调用方，同步是指被调用方得到结果之前不会返回，异步是指调用方立即得到返回，没有返回结果，通过回调函数得到实际结果
### 多线程与多进程
多线程均使用的一个物理CPU，经常与多进程搭配使用。多线程进行通信，多进程进行计算。
并发 多线程 线程交替
并行 多进程 多个进程同时执行
### 多线程创建
```python
import threading

def f(n):
    print(n)

t = threading.Thread(target=f,args=(1,))

class MyThread(threading.Thread):
    def __init__(self,n,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.n = n
    
    #  重写父类的run方法，在start时调用该方法
    def run(self):
        print(self.n)

t = MyThread(1)
t.start()
t.join()
```
#### 调试方法
```python
import threading
from time import sleep
def f(n):
    sleep(5)
    print(n)
t = threading.Thread(target=f,args=(1,))
# 判断线程是否存活 False
t.is_alive()

t.start()
t.is_alive() # True
t.join()
t.is_alive() # False
```
#### 线程锁
##### 普通锁和嵌套锁
```python
import threading
import threading
import time

num = 0

mutex = threading.Lock()
# mutex = threading.RLock()

def addone():
 global num
 time.sleep(1)
 if mutex.acquire(timeout=1):
     num += 1
     print(f'num value is {num}')
     # 普通Lock嵌套会产生死锁
     # mutex.acquire()
     # mutex.release()
 mutex.release()

for i in range(10):
 t = threading.Thread(target=addone)
 t.start()
```
##### 条件锁
   类似于生产者消费者模型
##### 信号量
同一时间最多启动多少个线程 threading.BoundedSemaphore(n)，超过数量的线程阻塞
```python
import time
import threading
 
def run(n):
    semaphore.acquire()
    print("run the thread: %s" % n)
    time.sleep(1)
    semaphore.release()

num = 0
semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
for i in range(20):
    t = threading.Thread(target=run,args=(i,))
    t.start()
```
##### 事件
##### 定时器
多长时间后运行该线程
#### 队列
线程安全，先进先出，主要方法：put()、get()、task_done()、join()等
```python
import queue
q = queue.Queue(5)
q.put(111)
q.put(222)
q.put(333)
print(q.get())
print(q.get())
q.task_done()
# 队列中元素个数
q.qsize()
q.empty()
q.full()

# 优先级队列
q = queue.PriorityQueue()
q.put((1,'work'))
q.put((-1,'life'))
q.put((1,'drink'))
q.put((-2,'sleep'))
print(q.get())
print(q.get())
print(q.get())
print(q.get())
```
### 线程池
使用concurrent包进行线程池创建，submit()或map()
```python
import time
from concurrent.futures.thread import ThreadPoolExecutor


def func(args):
    print(f'call func {args}')


if __name__ == '__main__':
    seed = ['a', 'b', 'c', 'd']
    with ThreadPoolExecutor(3) as executor1:
        # 参数原样传递到函数中
        executor1.submit(func, seed)

    time.sleep(1)

    with ThreadPoolExecutor(3) as executor2:
        # 参数映射到函数中
        executor2.map(func, seed)

    time.sleep(1)
```
***当回调已关联了一个 Future 然后再等待另一个 Future 的结果时就会发产死锁情况***

## 多进程与多线程抉择
由于python解释器的原因，一个进程内拥有一个GIL锁，同一时刻只能有一个线程运行，
通过线程的切换实现多线程并发， 在CPU密集型程序中推荐使用多进程，在IO密集型程序中，
推荐使用多线程。