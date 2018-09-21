# coding:utf-8
import os, commands

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
    return 0


def copy_module(ip, src, dest):
    '''
    cpoy module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    return 0


def unarchive_module(ip, src, dest):
    '''
    unarchive module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    return 0


def build_module(ip, dest):
    '''
    build module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh build ' + ip + ' ' + dest)
    return 0


def start_module(ip, dest):
    '''
    start module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh start ' + ip + ' ' + dest)
    return 0


def stop_module(ip, dest):
    '''
    stop module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    return 0


def check_module(ip, dest):
    '''check module
    check servers status
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh check ' + ip + ' ' + dest)
    return 0


def echo_module(ip, msg='HelloWorld!'):
    '''
    echo test module
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh echo ' + ip + ' ' + msg)
    print(status,type(status))
    print(result,type(result))
    get_result = result.split('\n')
    print(get_result,type(get_result))
    return 0


def monitor_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh monitor ' + ip + ' ' + dest)
    return 0


def environment_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    (status, result)=commands.getstatusoutput('bash ' + path.get_path() +
              '/scripts/ansible.sh environment ' + ip + ' ' + dest)
    return 0


if __name__ == '__main__':
    ansible_test()
