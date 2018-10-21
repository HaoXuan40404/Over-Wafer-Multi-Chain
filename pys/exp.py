# coding:utf-8
from pys.log import logger
from pys.log import consoler

class MCError(Exception):
    """Customize exception handling
    
    Arguments:
        Exception {string} -- exception description
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg
    
    def logout(self):
        consoler.info('%s', self.msg)
