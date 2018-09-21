# coding:utf-8
import os, commands, re
from pys.log import logger
from pys import path

class Ansible:
    """ansible配置
    """

    dir = '/data'

    def __repr__(self):
        return '[dir] %s' % (Ansible.dir)


def set_dir(dir):
    Ansible.dir = dir


def get_dir():
    return Ansible.dir


def ansible_test():
    ae = Ansible()
    set_dir('dir')
    print(ae)


def mkdir_module(ip, dest):
    '''
    mkdir module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh mkdir ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible mkdir_module action, error status => %s'% (status))
        logger.error('ansible mkdir_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible mkdir_module action, warn status => %s'% (status))
        logger.warn('ansible mkdir_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible mkdir_module action, info status => %s'% (status))
        logger.info('ansible mkdir_module action, info status => %s, info result => %s',status, result)
    return 0


def copy_module(ip, src, dest):
    '''
    cpoy module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    print(result)
    if status:
        print('ansible copy_module action, error status => %s'% (status))
        logger.error('ansible copy_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible copy_module action, warn status => %s'% (status))
        logger.warn('ansible copy_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible copy_module action, info status => %s'% (status))
        logger.info('ansible copy_module action, info status => %s, info result => %s',status, result)
    return 0


def unarchive_module(ip, src, dest):
    '''
    unarchive module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    print(result)
    if status:
        print('ansible unarchive_module action, error status => %s'% (status))
        logger.error('ansible unarchive_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible unarchive_module action, warn status => %s'% (status))
        logger.warn('ansible unarchive_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible unarchive_module action, info status => %s'% (status))
        logger.info('ansible unarchive_module action, info status => %s, info result => %s',status, result)
    return 0


def build_module(ip, dest):
    '''
    build module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh build ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible build_module action, error status => %s'% (status))
        logger.error('ansible build_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible build_module action, warn status => %s'% (status))
        logger.warn('ansible build_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible build_module action, info status => %s'% (status))
        logger.info('ansible build_module action, info status => %s, info result => %s',status, result)
    return 0


def start_module(ip, dest):
    '''
    start module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh start ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible start_module action, error status => %s'% (status))
        logger.error('ansible start_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible start_module action, warn status => %s'% (status))
        logger.warn('ansible start_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible start_module action, info status => %s'% (status))
        logger.info('ansible start_module action, info status => %s, info result => %s',status, result)
    return 0


def stop_module(ip, dest):
    '''
    stop module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible stop_module action, error status => %s'% (status))
        logger.error('ansible stop_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible stop_module action, warn status => %s'% (status))
        logger.warn('ansible stop_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible stop_module action, info status => %s'% (status))
        logger.info('ansible stop_module action, info status => %s, info result => %s',status, result)
    return 0


def check_module(ip, dest):
    '''check module
    check servers status
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh check ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible check_module action, error status => %s'% (status))
        logger.error('ansible check_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible check_module action, warn status => %s'% (status))
        logger.warn('ansible check_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible check_module action, info status => %s'% (status))
        logger.info('ansible check_module action, info status => %s, info result => %s',status, result)
    return 0


def echo_module(ip, msg='HelloWorld!'):
    '''
    echo test module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh echo ' + ip + ' ' + msg)
    print(result)
    if status:
        print('ansible echo_module action, error status => %s'% (status))
        logger.error('ansible echo_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible echo_module action, warn status => %s'% (status))
        logger.warn('ansible echo_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible echo_module action, info status => %s'% (status)s)
        logger.info('ansible echo_module action, info status => %s, info result => %s',status, result)
    return 0


def monitor_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh monitor ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible monitor_module action, error status => %s'% (status))
        logger.error('ansible monitor_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible monitor_module action, warn status => %s'% (status))
        logger.warn('ansible monitor_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible monitor_module action, info status => %s'% (status))
        logger.info('ansible monitor_module action, info status => %s, info result => %s',status, result)
    return 0


def environment_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh environment ' + ip + ' ' + dest)
    print(result)
    if status:
        print('ansible environment_module action, error status => %s' % (status))
        logger.error('ansible environment_module action, error status => %s, error result => %s',status, result)
    elif not (result.find('SUCCESS') + 1 ):
        print('ansible environment_module action, warn status => %s' %(status))
        logger.warn('ansible environment_module action, warning status => %s, warning result => %s',status, result)
    else:
        print('ansible environment_module action, info status => %s'% (status))
        logger.info('ansible environment_module action, info status => %s, info result => %s' ,status, result)
    return 0


if __name__ == '__main__':
    ansible_test()
