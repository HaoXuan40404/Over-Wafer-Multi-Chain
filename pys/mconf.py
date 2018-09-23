# coding:utf-8

import os
import sys
import configparser
import codecs
from pys import utils
from pys import path
from pys.log import logger


class MchainConf():
    """保存mchain.conf的配置
    """

    agent_name = 'WB'
    ansible_dir = '/data'
    sys_address = '0xe4cd3e488cbf0a98e8ecd8bc5eefaf10e5d54905'

    def __repr__(self):
        return '[agent_name] %s, [ansible_dir] %s, [sys_address] %s' % (MchainConf.agent_name, MchainConf.ansible_dir, MchainConf.sys_address)


def get_agent():
    return MchainConf.agent_name

def get_ansible_dir():
    return MchainConf.ansible_dir

def get_sysaddress():
    return MchainConf.sys_address


def parser(mchain):
    """解析mchain.conf配置文件
    
    Arguments:
        mchain {string} -- mchain.conf路径
    
    Raises:
        Exception -- 异常描述
    """

    logger.info('mchain.conf is %s', mchain)
    # 配置解析
    if not utils.valid_string(mchain):
        raise Exception('mchain not string ', mchain)

    # read and parser config file
    cf = configparser.ConfigParser()
    with codecs.open(mchain, 'r', encoding='utf-8') as f:
        cf.readfp(f)

    agent_name = cf.get('agent', 'agent_name')
    if not utils.valid_string(agent_name):
        raise Exception('invalid agent_name, ', agent_name)
    MchainConf.agent_name = agent_name

    ansible_dir = cf.get('ansible', 'dir')
    if not utils.valid_string(ansible_dir):
        raise Exception('invalid ansible_dir, ', ansible_dir)
    MchainConf.ansible_dir = ansible_dir

    logger.info('mchain.conf end, result is %s', MchainConf())
