#coding:utf-8

import os
from pys import path

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

def get_agent_ca_path():
    return CA.CA_path + '/' + CA.agent

def get_ca_path():
    return CA.CA_path

def root_ca_exist():
    return os.path.exists(CA.CA_path + '/ca.crt') and os.path.exists(CA.CA_path + '/ca.key')

def agent_ca_exist():
    return os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.crt') and os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.key')

def generate_root_ca(dir = CA.CA_path):

    os.environ['scripts'] = path.get_path() + '/scripts/'
    os.environ['out'] = dir
    os.system('bash $scripts/generate_chain_cert.sh -o $out')

def generator_agent_ca(dir, ca = CA.CA_path, agent = CA.agent):

    os.environ['scripts'] = path.get_path() + '/scripts/'
    os.environ['out'] = dir
    os.environ['ca'] = ca
    os.environ['agent'] = agent
    os.system('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent')

def generator_node_ca(dir, node, agent = CA.agent):

    os.environ['scripts'] = path.get_path() + '/scripts/'
    os.environ['agent'] = agent
    os.environ['node'] = node
    os.environ['out']= dir
    os.system('bash $scripts/generate_node_cert.sh -a $agent -d $agent -n $node -o $out')

def generator_sdk_ca(dir):
    os.environ['out'] = dir
    os.environ['scripts'] = path.get_path() + '/scripts/'
    os.system('bash $scripts/generate_sdk_cert.sh -d $out')
