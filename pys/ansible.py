# coding:utf-8
import commands
import os
import re

from pys import path
from pys.log import logger


class Ansible:
    """ansible配置, 用来配置推送的目标文件夹, default = '/data'
    """

    dir = '/data'

    def __repr__(self):
        return '[dir] %s' % (Ansible.dir)


def set_dir(dir):
    Ansible.dir = dir


def get_dir():
    return Ansible.dir


def mkdir_module(ip, dest):
    """调用ansible在目标服务器创建文件夹
    
    Arguments:
        ip {string} -- 目标服务器
        dest {string} -- 文件夹路径
    
    Returns:
        int -- 成功返回0, 否则返回-1.
    """

    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh mkdir ' + ip + ' ' + dest)
    logger.info('mkdir action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('mkdir action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('mkdir action failed, output %s' % (result))
    else:
        return 0
    return -1


def copy_module(ip, src, dest):
    '''
    cpoy module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    logger.info('copy action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('copy action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('copy action failed, output %s' % (result))
    else:
        return 0
    return -1


def unarchive_module(ip, src, dest):
    '''
    unarchive module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    logger.info('unarchive action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('unarchive action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('unarchive action failed, output %s' % (result))
    else:
        return 0
    return -1


def build_module(ip, dest):
    '''
    build module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh build ' + ip + ' ' + dest)
    logger.info('build action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('build action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('build action failed, output %s' % (result))
    else:
        return 0
    return -1


def start_module(ip, dest):
    '''
    start module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh start ' + ip + ' ' + dest)
    logger.info('start action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('start action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('start action failed, output %s' % (result))
    else:
        return 0
    return -1


def stop_module(ip, dest):
    '''
    stop module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    logger.info('stop action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('stop action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('stop action failed, output %s' % (result))
    else:
        return 0
    return -1



def check_module(ip, dest):
    """远程调用查看节点是否正常启动, 调用的是节点的check.sh
    
    Arguments:
        ip {string} -- 目标服务器
        dest {string} -- 远程调用目录
    
    Returns:
        int -- 成功返回0, 否则返回-1
    """

    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh check ' + ip + ' ' + dest)
    logger.info('check action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('check action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('check action failed, output %s' % (result))
    else:
        return 0
    return -1


def echo_module(ip, msg='HelloWorld!'):
    """调用ansible.sh echo模块, 使用ansible远程调用进行echo测试

    Arguments:
        ip {string} -- 服务器ip

    Keyword Arguments:
        msg {string} -- echo测试的字符串 (default: {'HelloWorld!'})

    Returns:
        [int] -- ansible正确调用echo返回0, 否则返回其他值.
    """
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh echo ' + ip + ' ' + msg)
    logger.info('echo action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('echo action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('echo action failed, output %s' % (result))
    else:
        return 0
    return -1


def monitor_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh monitor ' + ip + ' ' + dest)
    logger.info('monitor action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('monitor action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('monitor action failed, output %s' % (result))
    else:
        return 0
    return -1



def environment_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh environment ' + ip + ' ' + dest)
    logger.info('environment action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('environment action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('environment action failed, output %s' % (result))
    else:
        return 0
    return -1
