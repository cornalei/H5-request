import logging
import logging.config
from config.baseView import BaseView

CON_LOG='../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
class Common(BaseView):
    l_api = '/api/login'  # 登录接口
    profile='/api/sys/base/employee/profile'        #用户信息接口
    projiect='/api/biz/h5/in/project/my/select'     #内场项目列表接口

    # 登录外场工作台
    def loginOut(self,sql):
        phone = self.Dbfetchone(sql)[0]
        api='/api/verification/code/1/%s'%phone     #获取验证码接口
        form_data={"phone":phone,"loginType":6,"code":"6666"}
        #获取验证码
        self.getRequest(api)
        # 登录账号，提取token
        r1=self.postRequest(self.l_api,form_data).json()
        try:
            self.headers['X-Access-Token'] = r1['data']
        except BaseException:
            logging.error('未提取到登录token，登录接口返回%s' % r1)
        # 查询用户信息，提取用户所在组织架构ID
        r2 = self.getRequest(self.profile).json()
        try:
            self.headers['Eaton-ORG-ID'] = r2['data']['emp']['orgId']
        except BaseException:
            logging.error('未提取到orgId，接口返回%s' % r2)
        else:
            logging.info('外场工作台登录成功')

    # 登录内场工作台
    def loginIn(self,sql):
        phone=self.Dbfetchone(sql)[0]
        api = '/api/verification/code/1/%s' % phone  # 获取验证码接口
        form_data = {"phone": phone, "loginType": 6, "code": "6666"}
        # 获取验证码
        self.getRequest(api)
        # 登录账号，提取token
        r1 = self.postRequest(self.l_api, form_data).json()
        try:
            self.headers['X-Access-Token'] = r1['data']
        except BaseException:
            logging.error('未提取到登录token，登录接口返回%s'%r1)
        # 查询用户信息，提取用户所在组织架构ID
        r2 = self.getRequest(self.profile).json()
        try:
            self.headers['Eaton-ORG-ID'] = r2['data']['emp']['orgId']
        except BaseException:
            logging.error('未提取到orgId，用户信息接口返回%s'%r2)
        #获取用户所在项目列表
        r3=self.getRequest(self.projiect).json()
        try:
            self.headers['Eaton-Project-ID'] = r3['data']['select'][0]['id']
        except BaseException:
            logging.error('未提取到项目ID，项目列表接口返回%s'%r3)
        else:
            logging.info('内场工作台登录成功')




if __name__ == '__main__':
    # file = open('../config/data.yaml', 'r')
    # data = yaml.load(file, Loader=yaml.FullLoader)
    # phone = data['l_phone']
    sql = "select mobile from uc_user uu join uc_identity_employee uie " \
          "on uu.identity_id=uie.id join uc_organization uo " \
          "on uu.org_id=uo.id WHERE uo.`code`='CSGS' and uu.enabled_flag=1 and uie.position_status=0 LIMIT 0,1"
    sqlIn='''SELECT
	t.mobile
FROM
	(
		SELECT
			uu.mobile,
			up.data_scope,
			upg.group_type,
			up.position_type
		FROM
			uc_depart_position udp
		LEFT JOIN uc_user uu ON uu.id = udp.user_id
		LEFT JOIN uc_organization uo ON uo.id = uu.org_id
		LEFT JOIN uc_position up ON up.id = udp.position_id
		LEFT JOIN uc_position_group upg ON upg.id = up.group_id
		LEFT JOIN uc_identity_employee ui1 ON ui1.id = uu.identity_id
		WHERE
			udp.`delete` = 0
		AND uu.`delete` = 0
		AND uu.enabled_flag = 1
		AND ui1.position_status = 0
		AND position_id IN (
			SELECT
				urr.relation_id
			FROM
				uc_relation_role urr
			WHERE
				urr.`delete` = 0
			AND urr.role_id IN (
				SELECT
					ur.id
				FROM
					uc_role_per_relation urpr
				LEFT JOIN uc_role ur ON ur.`code` = urpr.role_code
				WHERE
					ur.`delete` = 0
				AND urpr.res_id = (
					SELECT
						um.id
					FROM
						uc_menu um
					WHERE
						um.`delete` = 0
					AND um. NAME = '项目管理-内场'
					AND um.module = 'STANDARDH5'
				)
			)
		)
		AND uo.`code` = 'CSGS'
	) t
LIMIT 0,
 1;'''

    S=Common()
    S.loginOut(sql)
    S.loginIn(sqlIn)