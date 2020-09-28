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