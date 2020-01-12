# -*- coding:utf-8 -*-

'''
封装HTTP请求操作
1. http_request是主方法，直接供外部调用
2. __http_get、__http_post是实际底层分类调用的方法
'''

import requests,os,logging
from kongling.common import opmysql
from logzero import logger


class RequestInterface(object):

    # 定义处理不同类别的请求参数，包含字典、字符串、空值
    def __new_parm(self,param):
        try:
            if isinstance(param,str) and param.startswith('{'):
                new_param = eval(param)
            elif param == None:
                new_param = ''
            else:
                new_param = param
        except Exception as error:
            new_param = ''

        return new_param

    # POST请求，参数在body中
    def __http_post(self,interface_url,interface_param):
        '''
        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return: 字典形式结构
        '''
        try:
            if interface_url!='':
                temp_interface_param = self.__new_parm(interface_param)
                response = requests.post(url=interface_url,data=temp_interface_param,verify=False,timeout=10)
                if response.status_code == 200:
                    durtime = response.elapsed.microseconds / 1000  # 发起请求和响应到达的时间，单位ms
                    result = {'code':'0000','message':'成功','data': response.text}
                else:
                    result = {'code': '1009','message': '接口返回状态错误','data': response.text}
            elif interface_url == '':
                result = {'code':'2004','message':'接口地址参数为空','data':[]}
            else:
                result = {'code':'2003','message':'接口地址错误','data':[]}
        except Exception as error:  # 记录日志到log.txt文件
            result = {'code':'9999','message':'系统异常','data':[]}
        return result

    # GET请求
    def __http_get(self,interface_url,interface_param):
        '''

        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return: 字典形式结果
        '''
        try:
            if interface_url != '':
                temp_interface_param = self.__new_parm(interface_param)
                # requrl = interface_url + temp_interface_param
                response = requests.get(interface_url,params=temp_interface_param, verify=False, timeout=10)
                # 打印出response
                if response.status_code == 200:
                    durtime = (response.elapsed.microseconds) / 1000  #  发起请求和响应到达的时间，单位为ms
                    result = {'code':"0000",'message':'成功','data':response.text}
                else:
                    result = {'code':'3004','message':'接口返回状态错误','data':[]}
            elif interface_url == '':
                result = {'code':'3002','message':'接口地址参数为空','data':[]}
            else:
                result = {'code':'3003','message':'接口地址报错','data':[]}

        except Exception as error:
            result = {'code':'9999','message':'系统异常','data':[]}
        return result

    # 判断请求类型
    def http_request(self,interface_url,interface_param,request_type):
        '''

        :param interface_url:  接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :param request_type: 请求类型
        :return: 字典形式结果
        '''
        try:
            if request_type == 'get' or request_type =='GET':
                result = self.__http_get(interface_url,interface_param)

            elif request_type == 'post' or request_type == 'POST':
                result = self.__http_post(interface_url,interface_param)
            else:
                result = {'code':'1000','message':'请求类型错误','data':[]}

        except Exception as error:
            result = {'code':'9999','message':'系统异常','data':[]}
        return result


if __name__ == '__main__':
    test_interface = RequestInterface()
    url='http://localhost:8081/getuser'
    interface_param = {}
    interface_result = test_interface.http_request(url,interface_param,'GET')
    if interface_result['code'] == '0000':
        logger.info(str(interface_result['data']))
    else:
        logger.info(str(interface_result['message']))
    test_db = opmysql.OperationDbInterface()
    sen_sq = "select exe_mode,url_interface,header_interface,params_interface from case_interface where name_interface='第一个demo接口' and id=1"
    params_interface = test_db.select_one(sen_sq)

