#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db=MySQLdb.connect('rm-wz96xqxw14qo6edaxio.mysql.rds.aliyuncs.com','hwy','HWY@112233','guan_uc',charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 查询语句
sql = "select mobile from uc_user uu join uc_identity_employee uie " \
      "on uu.identity_id=uie.id join uc_organization uo " \
      "on uu.org_id=uo.id WHERE uo.`code`='CSGS' and uu.enabled_flag=1 and uie.position_status=0 LIMIT 0,1"

try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      name = row[0]  #第一列
      # lname = row[1]  #第二列
      # age = row[2]
      # sex = row[3]
      # income = row[4]
      # 打印结果
      print ("账号为%s"%name)
except:
   print ("Error: unable to fecth data")

# 关闭数据库连接
db.close()