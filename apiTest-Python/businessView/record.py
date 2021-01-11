import random
from config.common import Common

class Record(Common):
    api1 = '/api/biz/h5/out/project/all/channel/select'     #查询项目列表接口
    api2 = '/api/biz/h5/out/putrecord/add'      #新增报备接口
    api3 = '/api/biz/ide/mark/createIdeMark'      #查询幂等id
    #报备参数
    assumpsitDate=Common().dateAdd(1)
    codCustPhone = random.randint(10000000, 99999999)


    sql = "select mobile from uc_user uu join uc_identity_employee uie " \
          "on uu.identity_id=uie.id join uc_organization uo " \
          "on uu.org_id=uo.id WHERE uo.`code`='CSGS' and uu.enabled_flag=1 and uie.position_status=0 LIMIT 0,1"

    def __init__(self):
        # 登录
        self.loginOut(self.sql)

    def outRecord(self):
        #查询可报备的项目，并提取项目id，name和公司id
        r1 = self.getRequest(self.api1).json()
        prjid = r1['data']['records'][0]['id']
        prjname = r1['data']['records'][0]['prjName']
        prjcomid = r1['data']['records'][0]['corpId']

        #查询幂等id
        param_data={'code':'putrecord'}
        r2=self.getRequest(self.api3,param_data).json()
        self.headers['idea-mark'] = r2['data']

        #新增报备
        form_data = {"namCustZh": "吴桂芳", "putrecordType": "1",
                     "codCustPhone": "130" + str(self.codCustPhone), "visitCount": "1",
                     "assumpsitDate": self.assumpsitDate + " 00:00:00",
                     "assumpsitTime": "3",
                     "codPrjId": prjid,
                     "codPrjName": prjname,
                     "codPrjCompanyId": prjcomid,
                     }
        return self.postRequest(self.api2,form_data)


if __name__ == '__main__':
    R=Record()
    R.outRecord()


