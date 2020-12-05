学习笔记
# 变量赋值
## 可变数据类型
- 列表 list 
- 字典 dict 
传递的是第一个数据的引用
内部数据变化会导致引用该对象的变量改变
## 不可变数据类型
- 整型 int
- 浮点型 float
- 字符串型 string
- 元组 tuple
不可变类型
## 序列
1. 容器序列（可以存放不同类型的数据）
    - 列表 list
    - 元组 tuple
    - 队列 collections.deque
2. 扁平序列（只能容纳一种类型的数据）
    - str
    - bytes
    - bytearray
    - memoryview 内存视图
    - array.array
    
### 拷贝问题
- 序列类型存在拷贝问题
- list()创建新的列表
- list[:]操作创建新的列表
### 浅拷贝和深拷贝
浅拷贝，只拷贝容器序列里面的内容，子序列不拷贝
深拷贝将容器序列里面所有的值重新申请内存，复制

    
## 非序列
- 字典

### 字典
- 通过hash函数进行散列
- 字典的key必须为不可变对象，只有不可变对象对应的hash值才确定
## collections基本数据类型扩展
### namedtuple
```python
import collections
Point = collections.namedtuple('Point',['x','y'])
p = Point(x=11,y=22)
print(p.x + p.y)
print(p)
```
### Counter
计数器，most_common统计topN
```python
from collections import Counter
mystring = ['a','b','c','d','d','d','d','c','c','e']
cnt = Counter(mystring)
# 建堆取最大
cnt.most_common(3)
print(cnt['b'])
```
### deque
双向队列
```python
from collections import deque

d = deque('uvw')
d.append('z')
print(d)
d.pop()
print(d)
d.appendleft('rst')
print(d)
d.popleft()
print(d)
```
## 魔术方法 （运算符重载）
```python
from collections import namedtuple
from math import sqrt

Point = namedtuple('Point', ['x', 'y', 'z'])


class Vector(Point):
    def __init__(self, p1, p2, p3):
        super(Vector).__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    # 重新定义减法
    def __sub__(self, other):
        tmp = (self.p1 - other.p1) ** 2 + (self.p2 - other.p2) ** 2 + (self.p3 - other.p3) ** 2
        return sqrt(tmp)


p1 = Vector(1, 2, 3)
p2 = Vector(4, 5, 6)
print(p1 - p2)

```
# 函数
## 可调用对象
```python
# 重载__call__()方法，实例可直接调用
class Kls1(object):
    def __call__(self):
        return 123


inst1 = Kls1()
inst1()
```
## 变量作用域
LEGB
- L-Local(function):函数内的命名空间
- E-Enclosing function locals:外部嵌套函数的命名控件（如closure）
- G-Global(module):函数定义所在模块（文件）的名字空间
- B-Builtin(Python):Python内置模块的命名空间
## 可变长参数
位置必须为最后传递的参数,先获取\*\*kwargs，再传递给\*args
```python
def func(*args, **kwargs):
    print(f'args: {args}')
    print(f'kwargs: {kwargs}')


func(123, 'xz', name='xvalue')
```
## 偏函数
固定函数的某些参数  
functools.partial:返回一个可调用的对象  
使用方法：partial(func,*args,**kwargs)
## 高阶函数
1. map
2. reduce
3. filter
4. partial
5. itertools.count()
## 函数返回值
### 返回关键字
- return
- yield
### 返回的对象
- 可调用对象--闭包（装饰器）
### 几个魔术方法
```python
def line_conf_v3():
    b = 10

    def line(x):
        """如果line()的定义中引用了外部的变量"""
        return 2 * x + b

    return line


b = -1
my_line = line_conf_v2()
print(my_line(5))

# 局部变量的名称
print(my_line.__code__.co_varnames)
# 自由变量的名称
print(my_line.__code__.co_freevars)
# 自由变量真正的值
print(my_line.__closure__[0].cell_contents)
```
### 闭包
函数和函数外部变量自由变量(nonlocal)的组成
#### 装饰器
增强而不改变原有函数  
装饰器强调函数的定义态而不是运行态
```python
@decorate
def target():
    print('do something')

def target():
    print('do something')
target = decorate(target)
```
```python
# 被装饰函数带参数
def outer(func):
    def inner(a, b):
        print(f'inner: {func.__name__}')
        print(a, b)
        func(a, b)

    return inner


@outer
def foo(a, b):
    print(a + b)
    print(f'foo: {foo.__name__}')


foo(1, 2)
print(foo.__name__)


# 被装饰函数带不定长参数
def outer2(func):
    def inner2(*args, **kwargs):
        func(*args, **kwargs)

    return inner2


@outer2
def foo2(a, b, c):
    print(a + b + c)


foo2(1, 2, 3)


# 被装饰函数带返回值

def outer3(func):
    def inner3(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret

    return inner3


@outer3
def foo3(a, b, c):
    return a + b + c


print(foo3(1, 3, 5))


# 装饰器带参数
def outer_arg(bar):
    def outer(func):
        def inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            print(bar)
            return ret

        return inner

    return outer


@outer_arg('foo_arg')
def foo(a, b, c):
    return a + b + c


foo(1, 3, 5)
```
##### 装饰器堆叠
从紧挨着函数向上进行处理
#### 内置装饰器
1. functools.wraps  
    通过@wraps修饰内部inner函数，达到与原函数名字保持一致的作用
2. functools.lru_cache
    通过lru算法对数据进行缓存
    ```python
    import functools
    
    @functools.lru_cache()
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 2) + fibonacci(n - 1)
    
    ```
    
#### 类装饰器
将类模拟成可调用对象
1. 通过__init__()方法接收装饰器的参数
2. 通过重写__call__()方法，传入函数对象，进行装饰器函数的编写
```python
from functools import wraps


class MyClass(object):
    # 装饰器参数同__init__进行接收
    def __init__(self, var='init_var', *args, **kwargs):
        self._v = var
        super(MyClass, self).__init__(*args, **kwargs)
    
    # 重写__call__方法，代替原装饰器方法
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            func_name = func.__name__ + " was called"
            print(func_name)
            return func(*args, **kwargs)

        return wrapped_function
```
#### 装饰器修饰类
传入类的对象到装饰器函数，通过重写对应函数进行扩展功能
```python
def decorate(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)

        def display(self):
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()

    return newClass


@decorate
class MyClass(object):
    def __init__(self, number):
        self.number = number

    def display(self):
        print("number is ", self.number)


six = MyClass(6)
for i in range(5):
    six.display()

```
#### dataclass
减少__init__()属性赋值的编写，通过@dataclass装饰器实现
```python
from dataclasses import dataclass


@dataclass
class MyClass:
    # 类属性
    a = 1
    # 实例属性，如果__init__(self)中只有属性赋值，可以用下面方式代替
    var_a: str
    var_b: str

    def abc(self):
        self.var_a = '123'

```
### yield
1. 在函数中使用 yield 关键字，可以实现生成器
2. 生成器可以让函数返回可迭代对象
3. yield和return不同，return返回后，函数状态终止，yield保持函数的执行状态  
返回后，函数回到之前保存的状态继续执行
4. 函数被yield会暂停，局部变量也会被保存
5. 迭代器终止时，会抛出 StopIteration 异常

- Iterables: 包含 \_\_getitem__() 或 \_\_iter__() 方法的容器对象
- Iterator: 包含 next() 和 \_\_iter__()方法
- Generator: 包含 yield 语句的函数

__Iterables > Iterator > Generator__
#### yield from
内层循环还可以迭代时使用，如果仍是可迭代对象即可使用yield from
```python
s = 'ABC'
t = [1, 2, 3]

def chain2(*iterables):
    for i in iterables:
        yield from i # 替代内层循环

print(list(chain2(s, t)))
```
#### 注意
1. 字典迭代器，对字典插入操作后，字典迭代器会立即失效
2. 尾插入操作不会损坏指向当前元素的List迭代器，列表会自动变长
3. 迭代器一旦耗尽，永久损坏
#### yield表达式
```python
def func():
    b = 0
    while True:
        a = yield b
        if a is None:
            a = 1
        b += a

if __name__ == '__main__':
    g = func()
    # next() 和 send(None)相同
    next(g)
    g.send(None)
    # send的值会传递给yield表达式等号前面的变量
    g.send(2)
```
## 对象协议
使用魔术方法描述对象
## Duck Typing
1. 容器类型协议
    - \_\_str__() 打印对象时，默认输出该方法的返回值
    - \_\_getitem__()、\_\_setitem__()、\_\_delitem__() 字典索引操作
    - \_\_iter__ 迭代器
    - \_\_call__ 可调用对象协议  
2. 比较大小的协议
    - \_\_eq__()
    - \_\_gt__()
3. 描述符协议和属性交互协议  
    - \_\_get__()
    - \_\_set__()
4. 可哈希对象
    - \_\_hash__()
5. 上下文管理器  
    with 上下文表达式的用法  
    使用\_\_enter__() \_\_exit__() 实现上下文管理器
# 协程
## 协程和线程的区别
- 协程是异步的，线程是同步的
- 协程是非抢占式的，线程是抢占式的
- 线程是被动调度的，协程是主动调度的
- 协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器
- 协程是用户级的任务调度，线程是内核级的任务调度
- 协程适用于IO密集型程序，不适合用于CPU密集型程序的处理

## await
1. await要放在函数当中
2. 函数需要被async关键字修饰
3. await 接收的对象必须是awaitable对象  
awaitable对象定义了 \_\_await__()方法
4. awaitable对象有三类：
    1. 协程 coroutine
    2. 任务 Task
    3. 未来对象 Future