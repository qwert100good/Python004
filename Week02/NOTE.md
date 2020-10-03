学习笔记

## 异常处理
### 处理异常过程
所有异常均继承自BaseException -> Exception
1. 异常类把错误消息打包到一个对象
2. 然后该对象会自动查找到调用栈
3. 直到运行系统找到明确声明如何处理这些类异常的位置

### 常见异常类
- IndexError KeyError
- IOError
- NameError
- TypeError
- AttributeError
- ZeroDivisionError

### 多个异常
使用(Exception1,Exception2)由小到大
```python
try:
    pass
except (IndexError,Exception) as e:
    pass
else:
    pass
finally:
    pass
```

### 自定义异常
继承自异常类，通过raise抛出，捕获自定义异常类
```python
class MyException(Exception):
    # 接收一个字符串参数
    def __init__(self,error_info):
        super().__init__(self, error_info)
        self.error_info = error_info

    def __str__(self):
        return self.error_info
        

try:
    raise MyException('用户输入错误')
except MyException as e:
    print(e)
```
### with语句块
通过修改类的 __enter__ __exit__方法实现自定义上下文管理器
```python
class Open:
    def __enter__(self):
        print('enter')

    # 固定参数 type，val，tracback
    # 如果with代码块中出现异常，可以这三个参数对异常进行捕获处理
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

with Open() as o:
    pass
```

## 数据库操作
### 安装pymysql
```shell script
pip install pymysql
```
### 基本使用流程
链接数据库connection->创建cursor->CURD(commit)->关闭cursor->关闭connection

### 注意事项
- 一个cursor就为一个事物
- 执行sql语句时，若进行数据修改。注意try except进行异常处理,使用conn.rollback()进行回滚防止数据异常

### 参数化执行
sql中使用%s占位，通过参数方式传入（避免SQL注入问题）
```python
import pymysql
db_info = {}
conn =pymysql.connect(**db_info)
cur = conn.cursor()
_id=1
cur.execute('SELECT * FROM tb WHERE id=%s',(_id,))
print(cur.fetchone())
cur.close()
conn.close()
```
批量执行 execute_many,参数为列表或元组[(),(),(),()]
```python
import pymysql
db_info = {}
conn =pymysql.connect(**db_info)
cur = conn.cursor()
vals=[(1,'a'),(2,'b'),(3,'c'),(4,'d')]
try:
    cur.executemany('INSERT INTO tb(`col1`,`col2`) VALUES (%s,%s)',vals)
    conn.commit()
except:
    conn.rollback()
cur.close()
conn.close()
```
### execute execute_many性能比对
- 通过execute_many批量执行sql进行数据插入执行时间**远远**小于多次调用execute执行sql
- 表中2个字段 col1(varchar(20)),col2 int 插入100000条测试数据
```python
import pymysql
conn = pymysql.conn()
cur = conn.cursor()
sql = 'INSERT INTO tb(`col1`,`col2`) VALUES (%s,%s)'
# 12s
for i in range(100000):
    value = (f'test{i}', str(i * 100))
    cur.execute(sql, value)
conn.commit()

# 1s
values = [(f'test{i}', str(i * 100)) for i in range(100000)]
cur.executemany(sql,values)
conn.commit()

```
## 反爬虫
### 浏览器基本行为
1. 带http头信息： User-Agent、Referer等
2. 带cookies(包含加密的用户名和密码验证信息)
#### 设置随机浏览器User-Agent
```python
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
# ua.chrome
# ua.safari
# ua.ie

# 随机返回头部信息
User_Agent = ua.random
```
设置Host或Referer内容添加到Headers中

#### 设置cookies
模拟用户登录
- requests通过session，先请求登录的url(post)，使session携带登录的cookies信息，再进行其他页面的请求
- scrapy通过start_url处理一次的方式，先请求登录的url(post)

#### 通过selenium的webdriver模拟浏览器行为
```python
from selenium import webdriver
# 需要配置对应浏览期的webdriver
browser = webdriver.Chrome()
```
## 文件下载
### 小文件直接读取存储
```python
import requests
# 小文件
image_url = 'xxxx.png'
r = requests.get(image_url)
with open('a.png','wb') as f:
    f.write(r.content)
```
### 大文件使用文件流方式
```python
import requests
pdf_url = 'xxx.pdf'
r = requests.get(pdf_url,stream=True)

with open('test.pdf','wb') as pdf:
    # iter_content方法为content的生成器
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```
## 验证码识别

### 环境配置
#### 安装tesseract
选择想要的版本安装 [下载地址](https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D)
#### 安装python依赖包
```shell script
pip install Pillow pytesseract
```

#### 处理验证码
利用Pillow对验证码图片进行灰度、二值化、降噪处理
使用pytesseract包调用tesseract对验证码图像进行识别
```python
from PIL import Image
import pytesseract

im = Image.open('demo.jpg')

# 灰度处理
gray = im.convert('L')

# 二值化
threshold = 100
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
out = gray.point(table, '1')

print(pytesseract.image_to_string(out, lang='chi_sim+eng'))

im.close()
```
识别不同类型的验证码，需要导入不同的训练集合。
[训练集](https://github.com/tesseract-ocr/tessdata)
下载后导入到 tesseract\tessdata 目录
## Scrapy代理设置
### 使用系统代理IP(只能代理一个ip)
1. export http_proxy = 'http://xxx.xxx.xxx.xxx:xx'(Linux,Mac),windows set http_proxy=xxx
2. setting增加scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
3. 通过 Request.meta['proxy'] 读取 http_proxy 环境变量加载代理
4. 直接在构造Request对象时传入meta['proxy]参数，进行代理

### 使用自定义中间件方法设置代理IP
下载中间件
```python
def process_request(request,spider):
    # request 对象经过下载中间件时会被调用，优先级高先调用
    pass
def process_response(request,response,spider):
    # response 对象经过下载中间件时会被调用，优先级高后调用
    pass
def process_exception(request,exception,spider):
    # 当process_response()和process_request()抛出异常时会被调用
    pass
def from_crawler(cls,crawler):
    # 使用 crawler 来创建中间器对象，并（必须）返回一个中间件对象
    pass
```
#### 继承系统的HttpProxyMiddleware，并且重写其中的from_crawler、__init__(self)、_set_proxy方法
```python
import random
from collections import defaultdict
from urllib.parse import urlparse
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured

class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    # 该中间件初始化方法，处理self.proxies属性
    def __init__(self,auth_encoding='utf-8',proxy_list=None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)
    
    # 读取配置文件，当作参数传入中间件的初始化方法中
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','utf-8')
        return cls(auth_encoding,http_proxy_list)
    
    # 随机选取self.proxies中的代理IP，写入request.meta中
    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```
#### 在settings配置文件中写入对应的代理IP列表并且添加自定义中间件
```python
HTTP_PROXY_LIST = [
   'http://124.205.155.152:9090',
   'http://115.171.85.189:8118',
   'http://124.205.155.154:9090'
]

DOWNLOADER_MIDDLEWARES = {
   'proxyspider.middlewares.ProxyspiderDownloaderMiddleware': 543,
   'proxyspider.middlewares.RandomHttpProxyMiddleware':400,
}
```