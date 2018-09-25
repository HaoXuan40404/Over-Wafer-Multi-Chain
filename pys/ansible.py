# coding:utf-8
import commands
import os
import re

from pys import path
from pys.log import logger
from pys.log import consoler


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
    logger.debug('mkdir action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('mkdir action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('mkdir action failed, output %s' % (result))
    else:
        return True
    return False


def copy_module(ip, src, dest):
    '''
    cpoy module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    logger.debug('copy action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('copy action failed, status %s' % (status))
        consoler.info('\t\t\t ansible copy opr failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.info('\t\t\t ansible copy opr failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
        logger.warn('copy action failed, output %s' % (result))
    else:
        consoler.info('\t\t\t ansible copy opr success, host is %s, src is %s, dst is %s.', ip, src, dest)
        return True
    return False


def unarchive_module(ip, src, dest):
    '''
    unarchive module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    logger.debug('unarchive action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('unarchive action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('unarchive action failed, output %s' % (result))
    else:
        return True
    return False


def build_module(ip, dest):
    '''
    build module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh build ' + ip + ' ' + dest)
    logger.debug('build action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('build action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('build action failed, output %s' % (result))
    else:
        return True
    return False


def start_module(ip, dest):
    '''
    start module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh start ' + ip + ' ' + dest)
    logger.debug('start action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('start action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('start action failed, output %s' % (result))
    else:
        return True
    return False


def stop_module(ip, dest):
    '''
    stop module
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    logger.debug('stop action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('stop action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('stop action failed, output %s' % (result))
    else:
        return True
    return False



def check_module(ip, dest):
    """远程调用查看节点是否正常启动, 调用的是节点的check.sh
    
    Arguments:
        ip {string} -- 目标服务器
        dest {string} -- 远程调用目录
    
    Returns:
        bool -- 成功返回Ture, 否则返回False
    """

    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh check ' + ip + ' ' + dest)
    logger.debug('check action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('check action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('check action failed, output %s' % (result))
    else:
        return True
    return False


def echo_module(ip, msg='HelloWorld!'):
    """调用ansible.sh echo模块, 进行echo测试, 判断ansible功能是否正常.

    Arguments:
        ip {string} -- 服务器ip

    Keyword Arguments:
        msg {string} -- echo测试的字符串 (default: {'HelloWorld!'})

    Returns:
        [bool] -- ansible正确调用echo返回True, 否则False.
    """
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh echo ' + ip + ' ' + msg)
    logger.debug('echo action , status %s, output %s' % (status, result))
   
    if status:
        consoler.info('\t\t\t [ERROR] ansible echo opr failed, host is %s, output is %s', ip, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.info('\t\t\t [ERROR] ansible echo opr failed, host is %s, output is %s', ip, result)
    else:
        consoler.info('\t\t\t ansible echo opr success, host is %s.', ip)
        return True
    return False


def monitor_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh monitor ' + ip + ' ' + dest)
    logger.debug('monitor action , status %s, output %s' % (status, result))
   
    if status:
        consoler.info('\t[ERROR] ansible echo opr failed, host is %s, output is %s', ip, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.info('\t[ERROR] ansible echo opr failed, host is %s, output is %s', ip, result)
    else:
        consoler.info('\t ansible echo opr success, host is %s.', ip)
        return True
    return False



def environment_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result) = commands.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh environment ' + ip + ' ' + dest)
    logger.debug('environment action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('environment action failed, status %s' % (status))
    elif not (result.find('SUCCESS') + 1):
        logger.warn('environment action failed, output %s' % (result))
    else:
        return True
    return False
