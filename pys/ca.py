#coding:utf-8

import os
from pys import path

class CA:
    '''
    save cert path、agency name
    '''
    CA_path = ''
    agent = ''

def set_agent(agent):
    """[set agency name]
    
    Arguments:
        agent {[string]} -- [agency name]
    """

    CA.agent = agent

def get_agent():
    """[get agency name]
    
    Returns:
        [string] -- [agency name]
    """

    return CA.agent

def set_ca_path(p):
    """[set cert path]
    
    Arguments:
        path {[path]} -- [cert path]
    """

    if not os.path.isdir(p):
        os.makedirs(p)
    CA.CA_path = p

def get_agent_ca_path():
    """[get agency cert path]
    
    Returns:
        [path] -- [agency cert path]
    """

    return CA.CA_path + '/' + CA.agent

def get_ca_path():
    """[get root cert path]
    
    Returns:
        [path] -- [root cert path]
    """

    return CA.CA_path

def get_GM_agent_ca_path():
    """[get gm agency cert path]
    
    Returns:
        [path] -- [agency cert path]
    """

    return CA.CA_path + '/GM/' + CA.agent

def get_GM_ca_path():
    """[get gm root cert path]
    
    Returns:
        [path] -- [root cert path]
    """

    return CA.CA_path + '/GM/'

def root_ca_exist():
    """[check root cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    
    return os.path.exists(CA.CA_path + '/ca.crt') and os.path.exists(CA.CA_path + '/ca.key')

def agent_ca_exist():
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """

    return os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.crt') and os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.key')

def generate_root_ca(dir):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """


    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.system('bash $scripts/generate_chain_cert.sh -o $out >/dev/null 2>&1')

def generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """


    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.environ['ca'] = ca
    os.environ['agent'] = agent
    os.system('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent >/dev/null 2>&1')

def generator_node_ca(dir, node, agent):
    """[generate node cert ]
    
    Arguments:
        dir {[path]} -- [node cert path]
        node {[string]} -- [node name]
        agent {[path]} -- [agency cert path]
    """

    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['agent'] = agent
    os.environ['node'] = node
    os.environ['out']= dir
    os.system('bash $scripts/generate_node_cert.sh -a $agent -d $agent -n $node -o $out >/dev/null 2>&1')

def generator_sdk_ca(dir):
    """[generate sdkcert ]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """

    os.environ['out'] = dir
    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.system('bash $scripts/generate_sdk_cert.sh -d $out')

def gm_generate_root_ca(dir):
    """[generate guomi root cert]
    
    Arguments:
        dir {[dir]} -- [put ca in dir]
    """
    
    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.system('bash $scripts/generate_chain_cert.sh -o $out -g')

def gm_generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """


    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.environ['ca'] = ca
    os.environ['agent'] = agent
    os.system('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent -g')

def gm_generator_node_ca(dir, node, agent):
    """[generate node cert ]
    
    Arguments:
        dir {[path]} -- [node cert path]
        node {[string]} -- [node name]
        agent {[path]} -- [agency cert path]
    """

    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['agent'] = agent
    os.environ['node'] = node
    os.environ['out']= dir
    os.system('bash $scripts/generate_node_cert.sh -a WB -d $agent -n $node -o $out -s sdk -g')
