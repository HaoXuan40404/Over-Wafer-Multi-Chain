#coding:utf-8
import os

from pys import path

class Ansible:
    '''
    ansible
    '''
    user = ''
    dir = '/data/'
    src_dir = ''

    def __repr__(self):
        return '[user] %s, [dir] %s' % (Ansible.user, Ansible.dir)


def set_user(user):
    Ansible.user = user


def set_dir(dir):
    Ansible.dir = dir

def get_dir():
    return Ansible.dir

def ansible_test():
    ae = Ansible()
    set_user('app')
    set_dir('dir')
    print(ae)


def mkdir_module(ip, dest):
    '''
    mkdir module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh mkdir ' + ip + ' ' + dest)
    return 0


def copy_module(ip, src, dest):
    '''
    cpoy module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    return 0


def unarchive_module(ip, src, dest):
    '''
    unarchive module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    return 0


def build_module(ip, dest):
    '''
    build module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh build ' + ip + ' ' + dest)
    return 0


def start_module(ip, dest):
    '''
    start module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh start ' + ip + ' ' + dest)
    return 0


def stop_module(ip, dest):
    '''
    stop module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    return 0


def check_module(ip, dest):
    '''check module
    check servers status
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh ' + ip + ' ' + dest)
    return 0


def test_module(ip, dest):
    '''
    test module
    '''
    os.system('bash ' + path.get_path() +
              '/scripts/ansible.sh ' + ip + ' ' + dest)
    return 0


def monitor_module(ip, dest):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    return 0


if __name__ == '__main__':
    ansible_test()
