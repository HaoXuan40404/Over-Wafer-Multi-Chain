#coding:utf-8

import re
import os
from pys.error.exp import MCError
from pys.log import logger
from pys.log import consoler
from pys.tool import utils

class Fisco:
    def __init__(self, fisco_path):
        self.fisco_path = fisco_path
        self.major = ''
        self.minor = ''
        self.revision = ''
        self.gm = False
        self.check_fisco_version()

    def __repr__(self):
        if self.gm:
            return 'fisco bcos : %s:%s:%s-%s' % (self.major, self.minor, self.revision, 'gm')
        else:
            return 'fisco bcos : %s:%s:%s' % (self.major, self.minor, self.revision)
    
    def is_13_version(self):
        return self.major == '1' and self.minor == '3'
    
    def is_15_version(self):
        return self.major == '1' and self.minor == '5'
    
    def is_20_version(self):
        return self.major == '2' and self.major == '0'
    
    def is_gm(self):
        return self.gm
    
    def get_fisco_path(self):
        return self.fisco_path
    
    def check_fisco_version(self):
         # check if fisco-bcos exists
        if not (os.path.exists(self.fisco_path) and os.path.isfile(self.fisco_path)):
            logger.error(' fisco-bcos not exist, fisco-bcos is %s', self.fisco_path)
            raise MCError(' fisco-bcos not exist, fisco-bcos is %s' % self.fisco_path)
        
        cmd = self.fisco_path + ' --version'
        status,output = utils.getstatusoutput(cmd)
        if status != 0:
            logger.error(' fisco-bcos --version failed, fisco-bcos is %s, status is %d, output is %s', self.fisco_path, status, output)
            raise MCError('fisco-bcos --version failed , fisco-bcos is %s.' % self.fisco_path)
        
        logger.debug(' fisco-bcos --version, status is %d, output is %s', status, output)
        
        version_info = output.split()
        if version_info[0] == 'FISCO-BCOS' and len(version_info) > 2:
            version = version_info[2].split('.')
            if not len(version) == 3:
                logger.error(' fisco-bcos --version invalid format, 00 status is %d, output is %s', status, output)
                raise MCError(' fisco-bcos --version invalid format , fisco-bcos is %s, version is %s.' % (self.fisco_path, version_info[2]))
            
            if version[2].endswith('-gm'):
                self.gm = True
            self.major = str(int(version[0]))
            self.minor = str(int(version[1]))
            if self.gm:
                self.revision = str(int(version[2][:-3]))
            else:
                self.revision = str(int(version[2]))

            logger.info(' fisco-bcos is %s', self)
            
        else:
            logger.error(' fisco-bcos --version invalid format, fisco-bcos is %s, status is %d, output is %s', self.fisco_path, status, output)
            raise MCError(' fisco-bcos --version invalid format , fisco-bcos is %s, status is %d, output is %s.' % (self.fisco_path, status, output))