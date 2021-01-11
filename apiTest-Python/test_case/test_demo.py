import requests,json,unittest,time,logging
from locust import HttpLocust,TaskSet,task

class SoundTest(unittest.TestCase):
    url = 'http://www30.1shuo.com/yishuo_30test/yishuo/api_web/live_app/get_live_sound_info'
    # @unittest.skip('test_sound')
    def test_sound(self):
        logging.info('====test_sound====')
        form_data = {'page': 1, 'per_page': 3}
        r=requests.post(self.url,data=form_data)
        response_data=r.json()

        self.assertEqual(response_data['msg'],'获取成功')
        self.assertEqual(response_data['code'],200)
        self.assertEqual(response_data['data']['list'][2]['name'],'马蹄声')

class UserBehavior(TaskSet):
    url = '/yishuo/api_web/live_app/get_live_sound_info'
    @task
    def test_sound(self):
        form_data = {'page': 1, 'per_page': 3}
        self.client.post(self.url,data=form_data)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    max_wait = 6000
    min_wait = 3000
    host = 'http://www30.1shuo.com/yishuo_30test'


if __name__ == '__main__':
    unittest.main()