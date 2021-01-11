import unittest,logging
from businessView.record import Record

class TestRecord(unittest.TestCase):
    # @unittest.skip('test_outRecord')
    def test_outRecord(self):
        r=Record().outRecord()
        try:
            self.assertEqual(r.status_code,200)
        except:
            logging.error('报备失败,响应内容为%s'%r)
        else:
            logging.info('报备成功')


if __name__ == '__main__':
    unittest.main()
