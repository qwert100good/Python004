学习笔记

# 类
## 属性
### 类属性（静态属性）
```python
class Human:
    live = True

    def __init__(self, name):
        self.name = name

# 查看该作用域下有什么属性和方法__dict__
Human.__dict__
# {'__module__': '__main__', 'live': True, '__init__': <function Human.__init__ at 0x0BBED780>, '__dict__': <attribute '__dict__' of 'Human' objects>, '__weakref__': <attribute '__weakref__' of 'Human' objects>, '__doc__': None}
```
### 实例属性
```python
class Human:
    live = True

    def __init__(self, name):
        self.name = name
# 查看属性的方法__dict__
man = Human('Adam')

man.__dict__
# {'name': 'Adam'}
```
### 属性相关操作
实例属性 优先于 类属性  
不存在的实例属性赋值时会创建新的属性
#### 查看属性的方法
1.  \_\_dict__
2. dir()
#### 为类添加属性
```python
setattr(class,'newattr','value')
```
#### _开头和__开头的属性
- _开头的属性为人为约定不可修改的属性
- __开头的属性系统会将其改名，实现为私有属性
#### __bases__查看父类,__subclasses__方法查看子类
```python
class.__class__.__bases__
object.__class__.__subclasses__
```
## 方法
### 三种方法类型
1. 实例方法  
第一个参数为self关键字，指实例化对象
2. 类方法  
    - 第一个参数为cls关键字，指该方法所在的类  
    - 需要添加@classmethod装饰器  
    - 类的实例和类均可以调用
3. 静态方法  
需要添加@staticmethod装饰器
#### 类方法 classmehtod
构造函数 直接调用类方法，代替原有的__new__()构造函数
- 定义在父类中，子类可以调用父类的classmethod对子类的变量进行修改
- 预处理函数，调用类并且返回实例对象的时候，类似于构造函数
#### 静态方法 staticmethod
与类和实例均无关，但是类中某些方法会使用的功能，定义为静态方法
## 属性描述符
### 实例获取属性的方法
1. __getattribute__方法
对所有属性的访问都会调用该方法
2. __getattr__方法  
针对于未定义的属性

两者都可以对实例属性进行获取拦截
###  __getattribute__方法和__getattr__方法同时存在
__getattribute__方法 > __getattr__方法 > __dict__方法
```python
class Human:
    def __init__(self, name):
        self.name = name


class Human2:
    def __init__(self):
        self.age = 18

    def __getattribute__(self, item):
        print(f'__getattribute__ called item:{item}')
        return super().__getattribute__(item)

    def __getattr__(self, item):
        print(f'__getattr__ called item:{item}')
        return 'Err 404,你请求的参数不存在'


h1 = Human2()
print(h1.age)
print(h1.noattr)
```
### 注意事项
1. 定义自己的__getattribute__方法会对实例化有性能损耗
2. 由于动态赋值，原有查找__dict__方法中属性的方法可能会出现不一致情况
## 描述器
通过属性函数或装饰器将方法修饰为属性
```python
# property(get_,set_,del_,'other property')
# @property
# @property.setter
# @property.deleter
```
### 建议和注意
- 被修饰的函数使用相同的函数名称
- 如果未定义setter方法，则进行改名 -> 类似于双下划线定义的属性
- property本质并不是函数，而是特殊类（实现了数据描述符的类）
## 元类
创建类的类为元类
### object和type的关系
- object和type都属于type类（class'type')
- type类由type元类自身创建的。
- object的父类为空，没有继承任何类
- type的父类为object类(class'type')
```python
# __class__打印由谁创建的类，__bases__打印继承关系
print('object', object.__class__, object.__bases__)
print('type', type.__class__, type.__bases__)
```
- 元类是创建类的类，是类的模板
- 元类是用来控制如何创建类的，正如类是创建对象的模板一样
- 元类的实例为类，正如类的实例为对象
- 创建元类的两种方法
    - class
    ```python
    def pop_value(self, dict_value):
        for key in self.keys():
            if self.__getitem__(key) == dict_value:
                self.pop(key)
                break
    
    
    # 元类要求，必须继承自type
    class DelValue(type):
        # 元类要求，必须实现new方法
        def __new__(cls, name, bases, attrs):
            attrs['pop_value'] = pop_value
            return type.__new__(cls, name, bases, attrs)
    
    
    class DelDictValue(dict, metaclass=DelValue):
        pass
    
    
    d = DelDictValue()
    d['a'] = 'A'
    d['b'] = 'B'
    d['c'] = 'C'
    d.pop_value('C')
    for k, v in d.items():
        print(k, v)
    ```      
    - type
    type(类名，父类的元组，包含属性的字典)
    ```python
    def hello(self):
    print('hello')
    
    c1 = type('Abc', (object,), {'hello': hello})
    c1().hello()
    ```
### 钻石继承时候的继承关系
画无环有向图，找入度为0的类，摘取该类后，再找入度为0的类，如果存在多个入度为0的类，从左边的类找起
也可以用mro()查看继承关系
## 设计模式
### 单例模式
### 工厂模式
#### 静态工厂模式
- 有一个工厂类
- 产品类（父类）
- 继承产品的类，一系列的类
- 通过向工厂类传入不同参数构造不同实例
#### 类工厂模式
动态生成类，并且添加某些方法
```python
def factory(func):
    class klass: pass
    setattr(klass, func.__name__,func)
    return klass

def say_foo(self):
    print('bar')

Foo = factory(say_foo)
foo = Foo()
foo.say_foo()
```
#### 抽象基类
抽象基类(abstract base class, ABC) 用来确保派生类实现了基类中的特定方法  
抽象基类的好处：
- 避免继承错误，使类层次易于理解和维护
- 无法实例化基类
- 如果忘记在其中一个子类中实现接口方法，要尽早报错
```python
from abc import ABC

class MyABC(ABC):
    pass

MyABC.register(tuple)

assert issubclass(tuple, MyABC)
assert isinstance((),MyABC)


from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def bar(self):
        pass


class Concreate(Base):
    def foo(self):
        pass

# TypeError: Can't instantiate abstract class Concreate with abstract methods bar
c = Concreate()

```
#### Mixin 模式
在程序运行过程中，重新定义类的继承，即动态继承。  
好处：
- 可以在不修改任何源代码的情况下，对已有类进行扩展
- 进行组件的划分
```python
class Displayer():
    def display(self, message):
        print(message)


class LoggerMixin():
    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        super(LoggerMixin, self).display(message)
        self.log(message)


class MySubClass(LoggerMixin, Displayer):
    def log(self, message):
        super().log(message, filename='subclasslog.txt')


subclass = MySubClass()
subclass.display('this string will be shown and logged in subclasslog.txt')
print(MySubClass.mro())

```