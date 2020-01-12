# -*- coding:utf-8 -*-

from kongling.common import request
import unittest
from logzero import logger

class TestRequest(unittest.TestCase):
    def setUp(self):
        logger.info('开始')

    def test_http_request(self):
        test_interface = request.RequestInterface()
        url='http://localhost:8081/getuser'
        interface_param = {}
        interface_result = test_interface.http_request(url,interface_param,'GET')
        # 添加断言
        self.assertEqual(interface_result['code'],0000,'接口返回值正常')
        self.assertEqual(interface_result['data']['age'],26,'接口关键值返回正常')

    def tearDown(self):
        logger.info('结束')


if __name__ == '__main__':
    unittest.main

