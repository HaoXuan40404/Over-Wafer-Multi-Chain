#coding:utf-8
import os

from pys import path, ansible


def start_module(chain_id, ip, index):
    '''
    start module
    '''
    dest = ansible.get_dir() + '/' + chain_id + '/'
    os.system('bash ' + path.get_path() +
              '/scripts/tools/nodeoperation.sh start ' + ip + ' ' + dest + ' ' + index)
    return 0


def stop_module(chain_id, ip, index):
    '''
    stop module
    '''
    dest = ansible.get_dir() + '/' + chain_id + '/'
    os.system('bash ' + path.get_path() +
              '/scripts/tools/nodeoperation.sh stop ' + ip + ' ' + dest + ' ' + index)
    return 0