#coding:utf-8
import os

class Ansible:
    '''
    ansible
    '''
    user = ''
    dir = ''
    src_dir = ''
    global ansible_path
    ansible_path = '../temp/'
     

    def __repr__(self):
        return '[user] %s, [dir] %s' % (Ansible.user, Ansible.dir)

def set_user(user):
    Ansible.user = user

def set_dir(dir):
    Ansible.dir = dir 

def ansible_test():
    ae = Ansible()
    set_user('app')
    set_dir('dir')
    print(ae)

def mdir_module(ip,dest):
    '''
    mkdir module
    '''
    os.system('bash ${ansible_path}ansible.sh shell ' + ip +  ' ' + dest)
    return 0

def copy_module(ip,src,dest):
    '''
    cpoy module
    '''
    os.system('bash ${ansible_path}ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    return 0


def unarchive_module(ip,src,dest):
    '''
    unarchive module
    '''
    os.system('bash ${ansible_path}ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    return 0


def build_module(ip,PATH):
    '''
    build module
    '''
    os.system('bash ${ansible_path}ansible.sh build ' + ip + ' ' + PATH)
    return 0


def start_module(ip,PATH):
    '''
    start module
    '''
    os.system('bash ${ansible_path}ansible.sh start ' + ip + ' ' + PATH)
    return 0


def stop_module(ip,PATH):
    '''
    stop module
    '''
    os.system('bash ${ansible_path}ansible.sh stop ' + ip + ' ' + PATH)
    return 0


def test_module(ip,PATH):
    '''
    test module
    '''
    os.system('bash ${ansible_path}ansible.sh this ' + ip + ' ' + PATH)
    return 0


def check_module(ip,PATH):
    '''check module
    check servers status
    '''
    return 0


def monitor_module(ip,PATH):
    '''monitor module
        monitor chains status including' 
        node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    return 0


if __name__ == '__main__':
    ansible_test()