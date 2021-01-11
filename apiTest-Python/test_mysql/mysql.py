import MySQLdb,yaml

#封装数据库操作
class DbMysql:
    file = open('../config/data.yaml', 'r')
    data = yaml.load(file, Loader=yaml.FullLoader)
    db = data['Uc']
    host=data['Host']
    user=data['User']
    passwd=data['Passwd']
    # （host：IP地址；prot：端口号；user：用户名；passwd：密码；db：数据库名称；charset：编码方式）
    def __init__(self,host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.db=db
        self.charset=charset
    #连接数据库
    def Dbconnect(self):
        self.DbCon=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.charset)
        # self.Dbcursor=self.DbCon.cursor(cursor=DbMysql.cursors.DictCursor)
        self.Dbcursor=self.DbCon.cursor()

    #查询（select）
    def Dbselect(self,selectsql):
        self.Dbconnect()
        try:
            self.Dbcursor.execute(selectsql)
            print("查询成功")
        except:
            print('查询出错，请排查问题。')
        # self.Dbclose()

    #查询返回一条数（fetchone）
    def Dbfetchone(self):
        fetchdata=self.Dbcursor.fetchone()
        self.Dbclose()
        return fetchdata

    #查询返回所有数据（fetchall）
    def Dbfetchall(self):
        fetchdata=self.Dbcursor.fetchall()
        self.Dbclose()
        return fetchdata

    # 返回前几行数据fetchmany
    def Dbfetchmany(self, num):
        fetchmanydata = self.Dbcursor.fetchmany(num)
        self.Dbclose()
        return fetchmanydata

    #获取影响的行数
    def Dbrowcount(self):
        rowcountdata=self.Dbcursor
        self.Dbclose()
        return rowcountdata

    #增加（insert）、修改（update）、删除（delete）,执行一条
    def Dbobj(self,sql):
        self.Dbconnect()
        try:
            self.Dbcursor.execute(sql)
            self.DbCon.commit()
            print('操作成功，请查看数据库数据。')
        except:
            print('操作出错，请排查问题。')
            self.DbCon.rollback()
        self.Dbclose()

    #增加（insert）、修改（update）、删除（delete）,执行多条
    def Dbobjmany(self,sql,params):
        self.Dbconnect()
        try:
            self.Dbcursor.executemany(sql,params)
            self.DbCon.commit()
            print('操作成功，请查看数据库数据。')
        except:
            print('操作出错，请排查问题。')
            self.DbCon.rollback()
        self.Dbclose()

    #关闭数据库
    def Dbclose(self):
        self.Dbcursor.close()
        self.DbCon.close()

if __name__ == '__main__':
    d=DbMysql()
    # #查询
    # sql='select * from bookinfo'
    # d.Dbselect(sql)
    # for i in d.Dbfetchall():
    #     print(i)

    # #同时插入多条数据-示例1
    # sql="insert into employee values(%s,%s,%s,%s,%s)"
    # params=[('lei','le',15,'n',5),('le','lei',15,'n',4)]
    # d.Dbobjmany(sql,params)

    # 同时插入多条数据-示例2
    sql = "select mobile from uc_user uu join uc_identity_employee uie " \
          "on uu.identity_id=uie.id join uc_organization uo " \
          "on uu.org_id=uo.id WHERE uo.`code`='CSGS' and uu.enabled_flag=1 and uie.position_status=0 LIMIT 0,1"

    d.Dbselect(sql)
    mobile=d.Dbfetchone()[0]
    print(mobile)