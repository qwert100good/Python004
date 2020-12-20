学习笔记

## URLconf-URL调度
### path和re_path实现
使用partial传递不同参数，重新生成的新函数
```python
path = partial(_path, Pattern=RoutePattern)
re_path = partial(_path, Pattern=RegexPattern)
```
### include()实现
通过判断传参，进行相应处理，解析后进行导入等操作
## View视图
### 处理用户请求
- request参数为HttpRequest类的实例对象
- request对象由wsgi处理后生成
- request对象包含有元信息META, GET, POST, COOKIES, FILES
### 获取GET请求的地址栏参数
```python
# request.GET -> QueryDict
def index(request):
    name = request.GET.get('name')
    return HttpResponse(f'Hello Django! - {name}')

```

### 进行内容返回
- 返回默认为HttpResponse对象
```python
from django.http import HttpResponse
# 空白的页面
response1 = HttpResponse()
# 可以自定义头部
response2 = HttpResponse("Any Text",content_type="text/plain")
```
- 返回为JsonResponse对象
```python
from django.http import JsonResponse
response3 = JsonResponse({'foo':'bar'})
```
## Model
### 为什么自定义的Model要继承 models.Model
- 不需要显示定义主键
- 自动拥有查询管理器对象
- 可以使用 ORM API对数据库、表实现 CRUD

### 查询管理器
#### 如何生成查询管理器
- Manager 继承自 BaseManagerFromQuerySet类，拥有 QuerySet的大部分方法，  
get、crate、filter等方法都来自QuerySet
- objects是Manager类的一个实例，继承自BaseManagerFromQuerySet类，  
BaseManagerFromQuerySet类是由BaseManager的from_queryset方法动态生成的  
并且该类能够使用QuerySet的方法
```python
@classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            # 添加了QuerySet类的方法
            **cls._get_queryset_methods(queryset_class),
        })
```
## 模板Template
### render方法
1. 获取真正的模板内容
2. 通过切割分成不同的组 ->  NodeList
3. 根据不同的组调用不同的render
 - TextNode 返回字符串本身
 - VariableNode 使用resolve() 通过语法解析器解析后返回
 - 解析成四种类型的token {{ 变量 {% 块 {# 注释 其他类型
## Django管理页面
1. python manager.py makemigrations 生成模型文件
2. python manager.py migrate 执行生成的migration文件
3. python manager.py createsuperuser 创建管理员
4. 进入admin.py 文件 导入并注册模型
    ```python
    from django.contrib import admin
    
    # Register your models here.
    from .models import Name
    
    admin.site.register(Name)
    ```
   
   
## 表单
使用Form对象定义表单
## auth
1. 通过form表单拿到对应用户名密码
2. 通过django.contrib.auth.authenticate 获取是否存在该用户
3. 如果存在该用户进行django.contrib.auth.login 登录，保持会话状态
views 视图
    ```python
    from django.contrib.auth import authenticate, login
    from django.http import HttpResponse
    from .form import LoginForm
    def login(request):
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 读取表单的返回值
                cd = login_form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user:
                    login(request, user)
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse('登录失败')
    ```
   
   
## 信号
```python
# 第一种方式，通过connect注册回调函数
def my_callback1(sender, **kwargs):
    print("request started!")


from django.core.signals import request_started

request_started.connect(my_callback1)

from django.core.signals import request_finished
from django.dispatch import receiver

# 第二种方式，通过装饰器注册回调函数

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("request finised!")

```
##  生产环境部署
1. Nginx
2. gunicorn
    - 安装gunicorn pipinstall gunicorn
    - 在项目目录执行 gunicorn xxx.wsgi
    - gunicorn 参数  
     -b 绑定ip和端口
     -w 多少个workers（进程数量=逻辑cpu核心）可以同时接受请求
     --access-logfile FILE 
     --access-logformat STRING 
     --error-logfile FILE 
     --log-level LEVEL
     
     
## Celery
- Celery 是分布式消息队列
- 使用Celery 实现定时任务  
    生产者：
    - 异步任务
    - 定时任务  
    
    消费者： 
    - 任务执行单元（程序）
    
    结果存储：
    - redis
### 注意
kombu包中存在async关键字命名的目录，需要进行替换
### django继承celery
1. Redis安装和启动  
redis-server /path/to/redis.conf
2. 安装Celery
    ```shell script
    pip install celery
    pip install redis==2.10.6
    pip install celery-with-redis
    pip install django-celery
    ```
3. 添加app
    ```shell script
    django-admin startproject MyDjango
    python manager.py startapp djcron
    ```
    settings.py
    ```python
    INSTALL_APPS = [
    'djceler',
    'djcron'
    ]
    ```
4. 迁移生成表
    ```shell script
    python manager.py migrate
    ```
5. 配置django时区 settings.py文件
    ```python
    from celery.schedules import crontab
    from celery.schedules import timedelta
    import djcelery
    djcelery.setup_loader()
    BROKER_URL = 'redis://127.0.0.1:6379' # 代理人
    CELERY_IMPORTS = ('djcron.tasks') # app
    CELERY_TIMEZONE = 'Asia/Shanghai' # 时区
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' #定时任务调度器
    ```
6. 在MyDjango下建立 celery.py
    ```python
    import os
    from celery import Celery, platforms
    from django.conf import settings
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULES', 'MyDjango.settings')
    app = Celery('MyDjango')
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    platforms.C_FORCE_ROOT = True
    ```
    在__init__.py增加
    ```python  
    # 使用绝对引入，后续使用import引入会忽略当前目录下的包
    from __future__ import absolute_import
    from .celery import app as celery_app
    ```
7. 添加定时任务
    ```python
    #在app下新建tasks
    from MyDjango.celery import app
    @app.task()
    def get_task():
        return 'test'
    
    @app.task()
    def get_task2():
        return 'test2'
    ```
8. 启动Celery
    ```shell script
    celery -A MyDjango beat -l info
    celery -A MyDjango worker -l info
    ```
