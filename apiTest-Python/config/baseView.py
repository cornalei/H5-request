import requests,time,json,yaml,MySQLdb,logging,os

class BaseView(object):
    path=os.path.abspath(os.path.join(os.path.dirname(__file__), './data.yaml'))
    file = open(path, 'r')
    # file = open('./data.yaml', 'r')
    data = yaml.load(file, Loader=yaml.FullLoader)
    #接口信息参数
    url=data['url']
    headers = {'Eaton-Company-CODE': data['Eaton-Company-CODE'],
               'Eaton-Origin': data['Eaton-Origin'],
               'Content-Type': data['Content-Type']
               }
    #数据库连接参数
    db = data['Uc']
    host = data['Host']
    user = data['User']
    passwd = data['Passwd']

    #获取时间
    def getTime(self):
        self.now=time.strftime("%Y%m%d-%H.%M.%S")
        return self.now
    #发起get请求
    def getRequest(self, api, *datas):
        if datas:
            return requests.get(self.url + api, headers=self.headers, params=datas[0])
        else:
            return requests.get(self.url + api, headers=self.headers)
    #发起post请求
    def postRequest(self, api, *datas):
        if datas:
            return requests.post(self.url + api, headers=self.headers, data=json.dumps(*datas))
        else:
            return requests.post(self.url + api, headers=self.headers)
    # 当前日期+n天
    def dateAdd(self, n):
        year = time.strftime("%Y-%m-", time.localtime())
        day = int(time.strftime("%d", time.localtime())) + n
        date = year + str(day)
        return date

    def Dbconnect(self):
        self.DbCon=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=3306,charset='utf8')
        # self.Dbcursor=self.DbCon.cursor(cursor=DbMysql.cursors.DictCursor)
        self.Dbcursor=self.DbCon.cursor()

    #查询（select）
    def Dbselect(self,selectsql):
        self.Dbconnect()
        try:
            self.Dbcursor.execute(selectsql)
            # print("查询成功")
        except:
            logging.error('查询出错，请排查问题!')

    #查询返回一条数（fetchone）
    def Dbfetchone(self,selectsql):
        self.Dbselect(selectsql)
        fetchdata=self.Dbcursor.fetchone()
        logging.info('登录账号为%s'%fetchdata)
        self.Dbclose()
        return fetchdata

    # 关闭数据库
    def Dbclose(self):
        self.Dbcursor.close()
        self.DbCon.close()

if __name__ == '__main__':
    d=BaseView()
    sql = "select mobile from uc_user uu join uc_identity_employee uie " \
          "on uu.identity_id=uie.id join uc_organization uo " \
          "on uu.org_id=uo.id WHERE uo.`code`='CSGS' and uu.enabled_flag=1 and uie.position_status=0 LIMIT 0,1"

    mobile = d.Dbfetchone(sql)[0]
    print(mobile)

