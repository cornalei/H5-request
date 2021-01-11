import MySQLdb

db=MySQLdb.connect('localhost','root','123456','book')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "insert into readerinfo(card_id,name,tel)values('210210199901022111','lisa','13544661111')"
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭数据库连接
db.close()