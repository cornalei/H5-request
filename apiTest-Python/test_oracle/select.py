#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cx_Oracle

# 打开数据库连接
db=cx_Oracle.connect('scott/123456@localhost:1521/orcl')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM emp"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      id = row[0]  #第一列
      name = row[1]  #第二列
      job = row[2]
      number = row[3]
      hiredate = row[4]
      # 打印结果
      print ("id=%s,name=%s,job=%s,number=%s,hiredate=%s" % (id, name, job, number, hiredate ))
except:
   print ("Error: unable to fecth data")

# 关闭数据库连接
db.close()