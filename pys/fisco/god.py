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
        (self.address, self.publicKey, self.privateKey) = self.load()

    def replace(self,genesis_path):
        (address, publicKey, privateKey) = ('', '', '')
        if self.fisco.is_gm():
            god_file = get_gm_god_path() + '/godInfo.txt' 
        else:
            god_file = get_god_path() + '/godInfo.txt'
        (address, publicKey, privateKey) = self.fromGod(god_file)
        utils.replace(genesis_path, self.address, address)
    
    def export(self):
        try:
            if self.fisco.is_gm():
                shutil.move(get_gm_god_path() + '/godInfo.txt',
                get_gm_god_path() + '/godInfo.txt.bak')
                cmd = self.fisco.get_fisco_path() + ' --newaccount ' + get_gm_god_path() + '/godInfo.txt'
                status, result = utils.getstatusoutput(cmd)
                logger.debug(' start status, status is %d, output is %s', status, result)
            else:
                shutil.move(get_god_path() + '/godInfo.txt',
                get_god_path() + '/godInfo.txt.bak')
                cmd = self.fisco.get_fisco_path() + ' --newaccount ' + get_god_path() + '/godInfo.txt'
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

        if self.fisco.is_gm():
            god_file = get_gm_god_path() + '/godInfo.txt'
        else:
            god_file = get_god_path() + '/godInfo.txt'

        return  self.fromGod(god_file)

    def fromGod(self, god_file):
        '''
        resolve .json, convert to config
        '''
        (address, publicKey, privateKey) = ('', '', '')
        try : 
            with open(god_file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith('address'):
                        address = line.split(':')[1].strip()
                    elif line.startswith('publicKey'):
                        publicKey = line.split(':')[1].strip()
                    elif line.startswith('privateKey'):
                        privateKey = line.split(':')[1].strip()
                logger.info(' god config success, file is %s, address is %s, publicKey : %s, privateKey : %s', 
                god_file, address, publicKey, privateKey)
                return  (address, publicKey, privateKey)
        except Exception as e:
            logger.error(' god config failed, cfg is %s, exception is %s', god_file, e)
            raise e




def god(fisco_path):
    god = God(fisco_path)
    god.export()
    god.replace('./')
    
    
    return 0

