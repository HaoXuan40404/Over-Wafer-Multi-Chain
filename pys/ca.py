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
    """[设置机构名称]
    
    Arguments:
        agent {[string]} -- [机构名称]
    """

    CA.agent = agent

def get_agent():
    """[获取机构名称]
    
    Returns:
        [string] -- [机构名称]
    """

    return CA.agent

def set_ca_path(p):
    """[设置证书路径]
    
    Arguments:
        p {[path]} -- [证书存放路径]
    """

    if not os.path.isdir(p):
        os.makedirs(p)
    CA.CA_path = p

def get_agent_ca_path():
    """[获取机构证书路径]
    
    Returns:
        [path] -- [机构证书路径]
    """

    return CA.CA_path + '/' + CA.agent

def get_ca_path():
    """[获取根证书路径]
    
    Returns:
        [path] -- [根证书路径]
    """

    return CA.CA_path

def root_ca_exist():
    """[判断根证书是否存在]
    
    Returns:
        [bool] -- [true为存在 false 为不存在]
    """
    
    return os.path.exists(CA.CA_path + '/ca.crt') and os.path.exists(CA.CA_path + '/ca.key')

def agent_ca_exist():
    """[判断机构证书是否存在]
    
    Returns:
        [bool] -- [true为存在 false 为不存在]
    """

    return os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.crt') and os.path.exists(CA.CA_path + '/'+ CA.agent + '/agency.key')

def generate_root_ca(dir):
    """[生成根证书]
    
    Arguments:
        dir {[path]} -- [根证书输出路径]
    """


    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.system('bash $scripts/generate_chain_cert.sh -o $out')

def generator_agent_ca(dir, ca, agent):
    """[生成机构证书]
    
    Arguments:
        dir {[path]} -- [机构证书输出路径]
        ca {[path]} -- [根证书存放路径]
        agent {[string]} -- [机构名称]
    """


    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    os.environ['ca'] = ca
    os.environ['agent'] = agent
    os.system('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent')

def generator_node_ca(dir, node, agent):
    """[生成节点证书]
    
    Arguments:
        dir {[path]} -- [节点证书输出路径]
        node {[string]} -- [节点名称]
        agent {[path]} -- [机构证书存放路径]
    """

    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['agent'] = agent
    os.environ['node'] = node
    os.environ['out']= dir
    os.system('bash $scripts/generate_node_cert.sh -a $agent -d $agent -n $node -o $out')

def generator_sdk_ca(dir):
    """[生成sdk证书]
    
    Arguments:
        dir {[path]} -- [机构证书路径]
        运行成功后会在目标路径下生成名为sdk的文件夹，内容为sdk证书
    """

    os.environ['out'] = dir
    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.system('bash $scripts/generate_sdk_cert.sh -d $out')
