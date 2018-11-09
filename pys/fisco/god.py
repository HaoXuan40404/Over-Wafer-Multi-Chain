#coding:utf-8

import os
import json
from pys.error.exp import MCError
from pys.log import logger
from pys.log import consoler
from pys.fisco.version import Fisco
from pys.tool import utils
import shutil



def set_god_path(p):
    """[set cert path]
    
    Arguments:
        path {[path]} -- [cert path]
    """

    if not os.path.isdir(p):
        os.makedirs(p)
    God.god_path = p

def get_god_path():
    """[get agency name]
    
    Returns:
        [string] -- [agency name]
    """

    return God.god_path + '/NA/'

def get_gm_god_path():
    """[get agency name]
    
    Returns:
        [string] -- [agency name]
    """

    return God.god_path + '/GM/'

class God:
    def __init__(self, fisco_path):
        self.fisco = Fisco(fisco_path)
        self.fisco_path = fisco_path
        self.address = ''
        self.publicKey = ''
        self.privateKey = ''
        self.load()
    
    def export(self):
        try:
            if self.fisco.is_gm():
                shutil.move(get_gm_god_path() + '/godInfo.txt',
                get_gm_god_path() + '/godInfo.txt.bak')
                cmd = self.fisco_path + ' --newaccount ' + get_gm_god_path() + '/godInfo.txt'
                status, result = utils.getstatusoutput(cmd)
                logger.debug(' start status, status is %d, output is %s', status, result)
            else:
                shutil.move(get_god_path() + '/godInfo.txt',
                get_god_path() + '/godInfo.txt.bak')
                cmd = self.fisco_path + ' --newaccount ' + get_god_path() + '/godInfo.txt'
                status, result = utils.getstatusoutput(cmd)
                logger.debug(' start status, status is %d, output is %s', status, result)
            if status != 0:
                logger.warn(' export godInfo.txt failed! status is %d, output is %s.', status, result)
                raise MCError('godInfo.txt failed! status is %d, output is %s.' % (status, result))
            logger.info(' export godInfo.txt status is %d, output is %s.', status, result)
            consoler.info(' export godInfo.txt success')
        except MCError as me:
            consoler.error(' \033[1;31m %s \033[0m', me)
        except Exception as e:
            consoler.error(' \033[1;31m export godInfo.txt failed! excepion is %s.\033[0m', e)
            logger.error('  export godInfo.txt failed!')

    def load(self):
        #os.path.exists(sjson)
        if self.fisco.is_gm():
            sjson = get_god_path() + '/godInfo.txt'
            print("sjson path is " + sjson)
            self.fromJson(sjson)
        else:
            sjson = get_gm_god_path() + '/godInfo.txt'
            print("sjson path is " + sjson)
            self.fromJson(sjson)

    def fromJson(self, sjson):
        '''
        resolve .json, convert to config
        '''
        result=[]
        try : 
            with open(sjson) as f:
                for line in f.readlines():
                    result.append(line)
                f.close()
                print result,type(result)
                address = result[1].split(':')[1]
                publicKey = result[2].split(':')[1]
                privateKey = result[3].split(':')[1]
                address = address.strip('\r\n')
                publicKey = publicKey.strip('\r\n')
                privateKey = privateKey.strip('\r\n')
                self.address = address
                self.publicKey = publicKey
                self.privateKey = privateKey
                consoler.debug(' god config success, file is %s, address is %s, publicKey : %s, privateKey : %s', sjson, str(self.address), str(self.publicKey), str(self.privateKey))
                return True
        except Exception as e:
            consoler.error(' god config failed, cfg is %s, exception is %s', sjson, e)
            return False


def god(fisco_path):
    god = God(fisco_path)
    god.export()
    return 0

