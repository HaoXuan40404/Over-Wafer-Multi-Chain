#coding:utf-8

import os

class CA:
    '''
    保存证书路径、机构名称
    '''
    CA_path = ''
    agent = ''

def set_agent(agent):
    CA.agent = agent

def get_agent():
    return CA.agent

def set_ca_path(p):
    if not os.path.isdir(p):
        os.makedirs(p)
    CA.CA_path = p

def get_ca_path():
    return CA.CA_path

def root_ca_exist():
    return os.path.exists(CA.CA_path + '/ca.crt') and os.path.exists(CA.CA_path + '/ca.key')

def agent_ca_exist():
    return os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.crt') and os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.key')
