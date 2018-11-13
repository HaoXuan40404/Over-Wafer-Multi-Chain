# coding:utf-8

import os
import sys
import configparser
import codecs
from pys.tool import utils
from pys import path
from pys.log import logger
from pys.error.exp import MCError


class MchainConf():
    """mchain.conf configuration
    """

    agent_name = 'FISCO'
    ansible_dir = '/data'
    sys_address = '0xe4cd3e488cbf0a98e8ecd8bc5eefaf10e5d54905'
    gm_sys_address = '0xee80d7c98cb9a840b9c4df742f61336770951875'

    def __repr__(self):
        return '[agent_name] %s, [ansible_dir] %s, [sys_address] %s, [gm_sys_address] %s' % (MchainConf.agent_name, MchainConf.ansible_dir, MchainConf.sys_address, MchainConf.gm_sys_address)


def get_agent():
    return MchainConf.agent_name

def get_ansible_dir():
    return MchainConf.ansible_dir

def get_sysaddress():
    return MchainConf.sys_address


def parser(mchain):
    """resolve mchain.conf
    
    Arguments:
        mchain {string} -- path of mchain.conf
    
    Raises:
        MCError -- exception description
    """

    logger.info('mchain.conf is %s', mchain)
    # resolve configuration
    if not utils.valid_string(mchain):
        logger.error(' mchain.conf not invalid path, mchain.conf is %s', mchain)
        raise MCError(' mchain.conf not invalid path, mchain.conf is %s' % mchain)

    # read and parser config file
    cf = configparser.ConfigParser()
    try:
        with codecs.open(mchain, 'r', encoding='utf-8') as f:
            cf.readfp(f)
    except Exception as e:
        logger.error(' open mchain.conf file failed, exception is %s', e)
        raise MCError(' open mchain.conf file failed, exception is %s' % e)

    agent_name = cf.get('agent', 'agent_name')
    if not utils.valid_string(agent_name):
        logger.error(' invalid mchain.conf format, agent_name empty, agent_name is %s', agent_name)
        raise MCError(' invalid mchain.conf format, agent_name empty, agent_name is %s' % agent_name)
    MchainConf.agent_name = agent_name

    ansible_dir = cf.get('ansible', 'dir')
    if not utils.valid_string(ansible_dir):
        logger.error(' invalid mchain.conf format, ansible_dir empty, ansible_dir is %s', ansible_dir)
        raise MCError(' invalid mchain.conf format, ansible_dir empty, ansible_dir is %s' % ansible_dir)
    MchainConf.ansible_dir = ansible_dir

    logger.info('mchain.conf end, result is %s', MchainConf())
