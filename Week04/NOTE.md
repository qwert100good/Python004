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
## 数据调整
### 数据范围选择
```python
import pandas as pd

df = pd.DataFrame()
# 多个列名使用列表
df[['A','C']]

# 选中某两列
df.iloc[:[0,2]]

# 多行选择 选择第1行和第3行
df.loc[[0,2]]

# 多行选择 选择第1行到第3行
df.loc[0:2]

# 条件选择
df[(df['A']<5) & (df['C']<4)]
```
### 数据替换
```python
import pandas as pd
import numpy as np

df = pd.DataFrame()
# 单个替换
df['C'].replace(4,40)
# 空值替换
df.replace(np.NAN,0)
# 多个替换
df.replace([4,5,6], 1000)
# 多对多替换
df.replace({4:400,5:500,8:800})
```
### 排序
```python
import pandas as pd
df = pd.DataFrame()
# 按照指定列降序排列
# ascending True 升序 False 降序
df.sort_values(by=['A'],ascending=False)
# 多列排序
df.sort_values(by=['A','C'],ascending=[True,False])
```
### 删除
```python
import pandas as pd
df = pd.DataFrame()
# 删除列
df.drop('A',axis=1)
# 删除行
df.drop(3,axis=0)
# 删除指定行(空值也成立）
df[df['A'] < 4]

# 行列互换，转置
df.T
df.T.T
```
### 数据透视表
```python
import pandas as pd
df = pd.DataFrame()
df4 = pd.DataFrame([
                     ['a', 'b', 'c'], 
                     ['d', 'e', 'f']
                    ],
                    columns= ['one', 'two', 'three'],
                    index = ['first', 'second']
                   )      
df4.stack()
df4.unstack()
# 重新生成索引
df4.unstack().reset_index()
```

# 数据计算
## 基本运算
```python
import pandas as pd

df = pd.DataFrame({
    "A": [5, 3, None, 4],
    "B": [None, 2, 4, 3],
    "C": [4, 3, 8, 5],
    "D": [5, 4, 2, None]
})
# 空值不参与运算仍为NaN
df['A'] + df['C']
df['A'] + 5

# 空值均为False
df['A'] < df['C']

# 统计数据
df.count()

# 聚合函数
df.sum()
df['A'].sum()
df.mean()
df.median()
```
## 分组聚合
分组后生成多个子DataFrame，每个子DataFrame包含符合要求的数据行
```python
import pandas as pd
import numpy as np

# 聚合
sales = [{'account': 'Jones LLC','type':'a', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co','type':'b',  'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc','type':'a',  'Jan': 50,  'Feb': 90,  'Mar': 95 }]

df2 = pd.DataFrame(sales)
# groups为分组内容，每组包含的行数
df2.groupby('type').groups
# 将计算结果进行合并
df2.groupby('type').agg({'type':'count','Feb':'sum'})
# 将计算结果映射到每个行中
df2.groupby('type').transform('mean')

# 数据透视表
# pd.pivot_table(data=,values=,index=,columns=,aggfunc=,margins=)
```
## 数据拼接
```python
import pandas as pd
import numpy as np
group = ['x','y','z']
data1 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10)
    })

data2 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "salary":np.random.randint(5,50,10),
    })

data3 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10),
    "salary":np.random.randint(5,50,10),
    })
pd.merge(data1,data2)
pd.merge(data2,data3,on='group')
# 指定左右表列
pd.merge(data3,data2,left_on='age',right_on='salary')
# 指定连接方式 inner left right outer
pd.merge(data3,data2,on='group',how='inner')

# 纵向连接
pd.concat([data1,data2])
```

# 输出
## 导出为excel
```python
import pandas as pd
import numpy as np
df = pd.DataFrame()
# 需要xlwt支持
df.to_excel('1.xlsx')
df.to_excel('2.xlsx',sheet_name='sheet1')
# 不输出索引 encoding指定字符编码
df.to_excel('2.xlsx',sheet_name='sheet1',index=False,encoding='utf-8')
# 指定列
df.to_excel('3.xlsx',sheet_name='sheet2',index=False,columns=['group','salary'])
# 导出到同一文件不同sheet页使用下面方式
with pd.ExcelWriter('2.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1', index=False)
    # 指定列
    df.to_excel(writer, sheet_name='sheet2', index=False, columns=['group', 'salary'])
```
## 导出为csv
to_csv()
## 导出为pkl文件
to_pickle()
## 可视化图形
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dates = pd.date_range('20200101', periods=12)
df = pd.DataFrame(np.random.randn(12, 4), index=dates, columns=list('ABCD'))

# plot 方法传入横坐标和纵坐标
plt.plot(df.index,df['A'])
# show 显示图像
plt.show()

# plot 可传参数 color linestyle linewidth marker
plt.plot(df.index, df['A'],
         color='#FFAA00',
         linestyle='-.-',
         linewidth=3,
         marker='D'
         )

import seaborn as sns

# 散点图
# 使用seaborn需要先声明类型，再生成图像
sns.set_style('darkgrid')
plt.scatter(df.index,df['A'])
plt.show()

```

# jieba分词
##使用cut函数进行拆分
1. 精确模式匹配
```python
import jieba
strings = ['我来自北京','今天天气真好']
for string in strings:
    jieba.cut(string,cut_all=False) 
```
2. 全模式匹配（搜索引擎搜索）
```python
import jieba
strings = ['我来自北京','今天天气真好']
for string in strings:
    jieba.cut(string,cut_all=True) 
```
3. 搜素
```python
import jieba
strings = ['我来自北京','今天天气真好']
for string in strings:
    result = jieba.cut_for_search(string)
    print('Search Mode:' + '/'.join(list(result)))
```
## 使用jieba.analyse进行关键词提取
### extract_tags，基于TF-IDF算法提取关键词
```python
import jieba.analyse

text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
# 基于TF-IDF算法进行关键词抽取
tfidf = jieba.analyse.extract_tags(text,topK=5,withWeight=True)
print(tfidf)
```
### textrank算法提取关键词
```python
import jieba.analyse

text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,topK=5,withWeight=True)
```
### 去除某些特定关键词
在txt中设置需要剔除的关键词 ex:
```text
需要
掌握
...
```
使用set_stop_words(文件路径)加载该文件
```python
import jieba.analyse
text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
tfidf = jieba.analyse.extract_tags(text, topK=5, withWeight=True)
jieba.analyse.set_stop_words(r'stop_word.txt')
textrank = jieba.analyse.textrank(text, topK=5, withWeight=True)
```
### 设置某些关键词
```python
import jieba
text = '极客大学Python进阶训练营真好玩'
# 加载关键词列表
jieba.load_userdict(r'user_dict.txt')
# 动态加载/删除
jieba.add_word('极客大学')
jieba.del_word('极客大学')
# 调整分词 合并分词
jieba.suggest_freq('中出',True)
# 调整分词 拆分分词 
# 合并和拆分需要关闭HMM后使用
jieba.suggest_freq(('中','出'),True)
print(list(jieba.cut(text, cut_all=False)))
```

# SnowNLP
```python
from snownlp import SnowNLP

text = 'xxxxxxxxxxxxxx'
s = SnowNLP(text)
# 情感倾向
print(s.sentiments)
```