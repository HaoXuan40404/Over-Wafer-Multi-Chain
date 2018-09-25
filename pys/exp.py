# coding:utf-8
from pys.log import logger
from pys.log import consoler

class MchainError(Exception):
    """自定义异常
    
    Arguments:
        Exception {string} -- 异常描述
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg
    
    def logout(self):
        consoler.info('%s', self.msg)
