# -*- coding: utf-8 -*-
"""
@author : Yx
"""

# SQL 转化 Pandas
'''
1. SELECT * FROM data;

2. SELECT * FROM data LIMIT 10;

3. SELECT id FROM data;  //id 是 data 表的特定一列

4. SELECT COUNT(id) FROM data;

5. SELECT * FROM data WHERE id<1000 AND age>30;

6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;

7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;

8. SELECT * FROM table1 UNION SELECT * FROM table2;

9. DELETE FROM table1 WHERE id=10;

10. ALTER TABLE table1 DROP COLUMN column_name;
'''
import pandas as pd
import pymysql
import numpy as np


def get_data_from_sql():
    con = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='w3h2')
    sql = 'SELECT * FROM job_info'
    df = pd.read_sql(sql, con)
    df.to_csv('ex.csv', index=False)


df = pd.read_csv('ex.csv')

# 1.SELECT * FROM data;
df1 = df
print(df1)

# 2.SELECT * FROM data LIMIT 10;
df2 = df.head(10)
print(df2)

# 3.SELECT id FROM data;
# 单列
# df3 = df['id']
# 多列
df3 = df[['id', 'company']]
print(df3)

# 4.SELECT COUNT(id) FROM data;
df4 = df['id'].count()
# Series
print(df4)

# 5.SELECT * FROM data WHERE id<1000 AND age>30;
# SELECT * FROM job_info WHERE id < 100 AND money > 20000;
df5 = df[(df['id'] < 100) & (df['money'] > 20000)].reset_index(drop=True)
print(df5)

# 6.SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
# 分组 使用size count展示所有列
df6 = df.groupby('id', as_index=False).size()
df6.columns = ['id', 'count']
print(df6)

# 7.SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(df)
df7_1 = df
df7_2 = df
# DataFrame1,DataFrame2列名相同，用on参数即可，否则需指定left_on,right_on
# df7 = df7_1.merge(df7_2, how='inner', on='id', suffixes=('_t1', '_t2'))
df7 = df7_1.merge(df7_2, how='inner', left_on='id', right_on='id', suffixes=('_t1', '_t2'))
print(df7)

# 8.SELECT * FROM table1 UNION SELECT * FROM table2
df8_1 = df
df8_2 = df
df8 = pd.concat([df8_1, df8_2]).reset_index()
print(df8)

# 9.DELETE FROM table1 WHERE id=10;
# 1. 取条件相反的数据集
df9_1 = df.loc[df['id'] != 10]
print(df9_1)
# 2. 先取出符合条件的index，再drop掉
df9_2 = df.drop(df[df['id'] == 10].index)
print(df9_2)

# 10.ALTER TABLE table1 DROP COLUMN column_name;
df10 = df.drop('id', axis=1)
print(df10)
