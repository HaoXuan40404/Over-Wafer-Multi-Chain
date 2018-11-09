#coding:utf-8

import re
import os
from pys.tool import utils
from pys.error.exp import MCError
from pys.log import logger
from pys.tool import utils

class JAVA:
    def __init__(self):
        self.major = ''
        self.minor = ''
        self.openjdk = False
        self.check_java()
    
    def is_suitable(self):
        version = int('%s%s' % (self.major, self.minor))
        return (version > 18) or ((version == 18) and (not self.is_openjdk()))
    
    def __repr__(self):
        if self.is_openjdk():
            return ' java version : %s.%s-%s' % (self.major, self.minor, 'openjdk')
        else:
            return ' java version : %s.%s-%s' % (self.major, self.minor, 'oracle')

    def is_openjdk(self):
        return self.openjdk
    
    def check_java(self):
        cmd = 'java -version'
        status,output = utils.getstatusoutput(cmd)
        if status != 0:
            logger.error(' java -version failed , status is %d, output is %s', status, output)
            raise MCError(' java -version failed , java not installed.')
        
        version_str = output.split("\"")
        if not len(version_str) > 1:
            logger.error(' cannot get java version, status is %d, output is %s', status, output)
            raise MCError(' cannot get java version, oracle jdk need >=1.8 or openjdk need >= 1.9, please try \'java -version\'. ')

        version_arr = version_str[1].split('.')
        if not len(version_arr) > 2:
            logger.error(' cannot get java version, status is %d, output is %s', status, output)
            raise MCError(' cannot get java version, oracle jdk need >=1.8 or openjdk need >= 1.9, please try \'java -version\' ')

        self.major = version_arr[0]
        self.minor = version_arr[1]
        if output.lower().find('openjdk') != -1:
            self.openjdk = True
        else:
            self.openjdk = False

        if not self.is_suitable():
            raise MCError(' invalid java version, oracle jdk need >=1.8 or openjdk need >= 1.9, now %s ' % self)
        
        logger.info(' java version is %s ', self)
        