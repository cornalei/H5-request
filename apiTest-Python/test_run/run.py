import unittest,time,logging
import logging.config
from BSTestRunner import BSTestRunner

#bat处理执行时使用
import sys
path='..' #文件所在根目录
sys.path.append(path)

#指定测试用例和测试报告的路径
test_dir='../test_case'
report_dir='../reports'

CON_LOG='../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()

def add_case():
    # 加载测试用例
    # discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')  # 匹配test开头的用例
    discover=unittest.defaultTestLoader.discover(test_dir,pattern='test_record.py')
    return discover

discover=add_case()
def run_case():
    #定义报告的文件格式
    now=time.strftime('%Y-%m-%d %H_%M_%S')
    report_name=report_dir+'/'+now+(' test_report.html')


    # 运行用例并生成测试报告
    with open(report_name,'wb') as f:
        runner=BSTestRunner(stream=f,title='接口测试报告',description='接口自动化测试报告')
        logging.info('start run test case...')
        runner.run(discover)



if __name__ == '__main__':
    run_case()
