from locust import HttpUser,TaskSet,task

class UserBehavior(TaskSet):
    def on_start(self):
        #设置user参数下标初始值
        self.users_index=0

    @task
    def test_users(self):
        #读取参数
        users_id=self.locust.id[self.users_index]
        url='/users/'+str(users_id)+'/'
        self.client.get(url,auth=('leilani','lei123456'))
        #取余运算循环遍历参数
        self.users_index=(self.users_index+1)%len(self.locust.id)

class WebsiteUser(HttpUser):
    task_create = UserBehavior
    #参数配置
    id=[1,2]
    min_wait = 3000
    max_wait = 6000
    #host配置
    host = 'http://127.0.0.1:8000'