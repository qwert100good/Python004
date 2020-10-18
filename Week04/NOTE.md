学习笔记

# 数据准备
## 基本数据类型
### Series
#### 基本属性
1. index
2. value
#### 创建方式
```python
import pandas as pd
import numpy as np

s = pd.Series(['a','b','c'])
s1 = pd.Series({'a': 11, 'b': 22, 'c': 33})
s2 = pd.Series([11, 22, 33], index=['a', 'b', 'c'])
```
#### 索引
使用index会提升查询性能
1. index唯一，使用哈希表优化，查询效率为O(1)
2. index有序不唯一，pandas使用二分查找算法，查询效率为O(logN)
3. index完全随机，每次需要扫描全表，查询效率为O(N)

获取index
- s.index
#### 数据

- 类型为np.ndarray
- s.values
- 转化为列表 s.values.tolist()
- map()进行对整列数据进行处理

### DataFrame
#### 创建方式
```python
import pandas as pd

df1 = pd.DataFrame(['a', 'b', 'c', 'c'])
df2 = pd.DataFrame([
    ['a', 'b'],
    ['c', 'd']
])
# 自定义行索引
df2.columns = ['one', 'two']
# 自定义列索引
df2.index = ['first', 'second']

df3 = pd.DataFrame([
    ['a', 'b'],
    ['c', 'd']],index=['first', 'second'],columns=['one', 'two'])
```
#### 索引
- 行索引 df.index
- 列索引 df.columns
 
#### 数据
- 类型为np.ndarray
- df.values
- 转化为列表 df.values.tolist()
- 显示前多少行 df.head()
- 行列数量返回(rows,cols) df.shape
- 详细信息 df.describe() df.info()
- map()进行对整列数据进行处理

## 引入外部数据
### 导入csv
```python
import pandas as pd
# 可以设置分隔符，行数等
pd.read_csv('1.csv',sep='',nrows=10,encoding='utf-8')
```
### 导入excel
```python
import pandas as pd
# 需要xlrd库
# sheet_name参数，数字为index，或者字符串sheet_name
pd.read_excel('1.xlsx',sheet_name=0)
```
### 导入sql数据
```python
import pandas as pd
import pymysql
# 需要传入一个连接和对应sql
conn = pymysql.Connect(host='localhost', user='root', password='123456', database='w3h2')
sql = 'SELECT 1'
pd.read_sql(sql=sql,con=conn)
```

# 数据预处理
## 缺失值处理
### Series
```python
import pandas as pd
import numpy as np

x = pd.Series([1,2,np.nan,3,4,5,6,np.nan,8])
# 判断数据是否由缺失值
x.hasnans
# 使用均值填充,inplace参数可选择是否原地修改默认为False会生成新的DataFrame对象
x.fillna(value=x.mean())
```
### DataFrame
```python
import pandas as pd
df=pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
# 查看缺失值
# 返回一个大小相同的Boolean类型DataFrame显示是否为缺失值
# 使用sum()进行统计，可以传递axis默认为0，0 列 1 行
print(df.isna().sum())
# 使用上一行数据填充
df.ffill()
# 使用上一列数据填充
df.ffill(axis=1)
# 删除缺失值,整行
df.dropna()
# 填充固定值
df.fillna('无')
```
## 重复值处理
删除重复值 通过df.drop_duplicates()删除整行记录
- subset 列名
- keep 保留哪些数据 'first' 或 'last' 或 False