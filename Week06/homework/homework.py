# if __name__ == '__main__':
#     # 实例化动物园
#     z = Zoo('时间动物园')
#     # 实例化一只猫，属性包括名字、类型、体型、性格
#     cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
#     # 增加一只猫到动物园
#     z.add_animal(cat1)
#     # 动物园是否有猫这种动物
#     have_cat = hasattr(z, 'Cat')
# 定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
# 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
# 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
# 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @property
    @abstractmethod
    def disposition(self):
        pass

    @property
    @abstractmethod
    def is_fierce_animal(self):
        pass


class SomeAnimal(Animal):
    call = ''

    def __init__(self, name, type, size, disposition):
        self._name = name
        self._type = type
        self._size = size
        self._disposition = disposition

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        if self._type == '食肉':
            _type = 1
        else:
            _type = 0
        return _type

    @property
    def size(self):
        if self._size == '小':
            size = 1
        elif self._size == '中等':
            size = 2
        elif self._size == '大':
            size = 3
        else:
            size = 0
        return size

    @property
    def disposition(self):
        if self._disposition == '凶猛':
            disposition = 1
        else:
            disposition = 0
        return disposition

    @property
    def is_fierce_animal(self):
        if self.size >= 2 and self.type == 1 and self.disposition == 1:
            return True
        return False

    @property
    def is_pet(self):
        if self.disposition == 1:
            return False
        return True


class Cat(SomeAnimal):
    call = '喵喵喵'


class Dog(SomeAnimal):
    call = '汪汪汪'


class Zoo(object):

    def __init__(self, name):
        self._name = name

    def __getattr__(self, item):
        try:
            self.__getattribute__(item)
        except AttributeError:
            return None
        return self.__getattribute__(item)

    @property
    def name(self):
        return self._name

    def add_animal(self, animal):
        if not self.__getattr__(animal.__class__.__name__) and isinstance(animal, Animal):
            self.__setattr__(animal.__class__.__name__, animal)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    dog1 = Dog('狗子', '食肉', '大', '凶猛')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 增加一只狗到动物园
    z.add_animal(dog1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    have_dog = hasattr(z, 'Dog')
    print(f'动物园有猫 {have_cat} {z.Cat.name}')
    print(f'动物园有狗 {have_dog} {z.Dog.name}')
    print(z.Cat.call)
    print(z.Dog.call)
    print(f'Cat 是凶猛动物 {z.Cat.is_fierce_animal}')
    print(f'Cat 是宠物 {z.Cat.is_pet}')
    print(f'Dog 是凶猛动物 {z.Dog.is_fierce_animal}')
    print(f'Dog 是宠物 {z.Dog.is_pet}')
