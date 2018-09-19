#coding:utf-8

import os
import sys
import configparser
import codecs
from pys import utils
from pys import path
from pys.log import logger

class MchainConf():
    '''
    mchain
    '''
    user_name = ''
    mchain_dir = './conf/mchain.conf'
    agent_name = ''
    contract_sysaddress = ''


    def __repr__(self):
        return '[user] %s, [dir] %s' % (MchainConf.user_name, MchainConf.mchain_dir)





def get_dir():
    return MchainConf.mchain_dir

def get_user():
    return MchainConf.user_name

def get_agent():
    return MchainConf.agent_name

def get_contract_sysaddress():
    return MchainConf.contract_sysaddress  



def mchain_conf(mchain):
    '''
    解析mchain.conf配置
    '''
    logger.info('mchain.conf is %s', mchain)
     # 配置解析
    if not utils.valid_string(mchain):
            raise Exception('mchain not string ', mchain)
    logger.info('mchain parser %s', mchain)
    # read and parser config file
    cf = configparser.ConfigParser()
    with codecs.open(mchain, 'r', encoding='utf-8') as f:
        cf.readfp(f)

    agent_name = cf.get('agent', 'agent_name')
    if not utils.valid_string(agent_name):
        raise Exception('invalid agent_name, ', agent_name)
    MchainConf.agent_name = agent_name

    user_name = cf.get('ansible', 'user')
    if not utils.valid_string(user_name):
        raise Exception('invalid user_name, ', user_name)
    MchainConf.user_name = user_name

    mchain_dir = cf.get('ansible', 'dir')
    if not utils.valid_string(mchain_dir):
        raise Exception('invalid mchain_dir, ', mchain_dir)
    MchainConf.mchain_dir = mchain_dir

    contract_sysaddress = cf.get('contract', 'sysaddress')
    if not utils.valid_string(contract_sysaddress):
        raise Exception('invalid contract_sysaddress, ', contract_sysaddress)
    MchainConf.contract_sysaddress = contract_sysaddress
    logger.info('mchain.conf end')


    return 0




    


    
    

