# 作业一：
#
# 区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
#
# list
# tuple
# str
# dict
# collections.deque
# 作业二：
# 自定义一个 python 函数，实现 map() 函数的功能。
#
# 作业三：
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。

# 作业一：
# 容器序列：list, tuple, collections.deque
# 扁平序列: str
# 可变序列: list, collections.deque
# 不可变序列: str, tuple
# 非序列: dict


# 作业二:
from collections.abc import Iterable, Callable


# 自定义map函数
def func(fun: Callable, it: Iterable):
    if not isinstance(fun, Callable):
        raise TypeError('arg 1 must be type Callable')
    if not isinstance(it, Iterable):
        raise TypeError('arg 2 must be type Iterable')
    for item in it:
        yield fun(item)


# 作业三
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        cost = (end_time - start_time) * 1000
        print(f'function {func.__name__} cost {cost}ms')
        return result

    return wrapper


@timer
def foo(num):
    sum = 0
    for i in range(num):
        sum += 1
    return sum
