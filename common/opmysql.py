# -*- coding: utf-8 -*-
'''
定义对数据库的基本操作的封装
1. 包括对单条语句操作，删除、修改、更新
2. 独立的查询单条、多条语句
3. 独立地添加多条语句
'''

import pymysql
from logzero import logger
from pymysql.cursors import DictCursor


class OperationDbInterface(object):
    def __init__(self,host_db='127.0.0.1',user_db='root',passwd_db='kongling21!',name_db='test_interface',port_db=3306):
        '''

        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整型数字
        :param link_type: 连接类型，用于输出的数据是元组还是字典，默认是字典，link_type=0
        :return:游标
        '''
        try:
            self.conn = pymysql.connect(host=host_db,user=user_db,passwd=passwd_db,db=name_db,port=port_db,charset='utf8')  # 创建数据库连接

            self.cur = self.conn.cursor(cursor=DictCursor)  # 返回字典
        except pymysql.Error as e:
            logger.info('创建数据库连接失败|Mysql Error %d:%s' % (e.args[0]),e.args[1])
            # logging.basicConfig(filename= public.config.src_path + '/log/sys.error.log',level = logging.DEBUG, format='%(asctime)s %(filename)')
            # logger1 = logging.getLogger(__name__)
            # logger1.exception(e)

    def op_sql(self,condition):
        '''

        :param condition: SQL语句，该通用方法可用来代替 insertone、updateone、deleteone
        :return: 字典形式
        '''
        try:
            self.cur.execute(condition)
            self.conn.commit()
            result = {'code':'0000','message':'执行通用操作成功','data':[]}
        except pymysql.Error as e:
            self.conn.rollback()  # 执行回滚操作
            result = {'code':'9999','message':'执行通用操作异常','data':[]}
        return result
    #  查询表中单条数据
    def select_one(self,condition):
        '''

        :param condition: sql语句
        :return: 字典形式的单条查询结果
        '''
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                results = self.cur.fetchone()
                result = {'code':'0000','message':u'执行单条查询操作成功','data':results}
            else:
                result = {'code':'0000','message':u'执行单条查询成功'}

        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code':'9999','message':'执行单条查询异常','data':[]}

        return result

    def select_all(self,condition):
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:
                results = self.cur.fetchall()
                result = {'code':'0000','message':u'执行批量查询操作成功','data':results}
            else:
                result = {'code':'0000','message':u'执行批量查询操作成功','data':[]}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code':'9999','message':'执行批量查询异常','data':[]}

        return result

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()


if __name__ == "__main__":
    test = OperationDbInterface()
    sen_sql = 'select * from case_interface where case_status=1 and name_interface="/getuser" and exe_level in (0,1,2)'
    result = test.select_all(sen_sql)
    if result['code'] == '0000':
        logger.info(str(result['data']))
    else:
        logger.info(str(result['message']))



