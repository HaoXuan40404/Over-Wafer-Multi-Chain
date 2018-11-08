#coding:utf-8

import shutil
import os

from pys import utils
from pys import path
from pys.log import logger
from pys.log import consoler
from pys.chain.parser import ConfigConfs
import configparser
from pys.exp import MCError
import sys

class CA:
    '''
    save cert path and agency name
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

    return CA.CA_path + '/NA/' + CA.agent + '/'

def get_ca_path():
    """[get root cert path]
    
    Returns:
        [path] -- [root cert path]
    """

    return CA.CA_path + '/NA/'

def get_GM_agent_path():
    """[get gm agency cert path]
    
    Returns:
        [path] -- [agency cert path]
    """

    return CA.CA_path + '/GM/' + CA.agent + '/'

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
    
    return os.path.exists(get_ca_path() + '/ca.crt') and os.path.exists(get_ca_path() + '/ca.key')

def root_gmca_exist():
    """[check root cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    
    return os.path.exists(get_GM_ca_path() + '/gmca.crt') and os.path.exists(get_GM_ca_path() + '/gmca.key')

def agent_ca_exist():
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """

    return os.path.exists(get_ca_path() + '/'+ CA.agent + '/agency.crt') and os.path.exists(get_ca_path() + '/'+ CA.agent + '/agency.key')

def agent_gmca_exist():
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """

    return os.path.exists(get_GM_ca_path() + '/'+ CA.agent + '/gmagency.crt') and os.path.exists(get_GM_ca_path() + '/'+ CA.agent + '/gmagency.key')



def generate_root_ca(dir):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """
    try:
        dir = os.path.abspath(dir)
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/cts.sh gen_chain_cert ' + dir)
        if status != 0:
            logger.warn(' cts.sh failed! status is %d, output is %s, dir is %s.', status, result, dir)
            raise MCError('cts.sh failed! status is %d, output is %s, dir is %s.' % (status, result, dir))
        logger.info(' cts.sh success! status is %d, output is %s, dir is %s.', status, result, dir)
        logger.info(' Generate root cert success, dir is %s', dir)
        consoler.info(' Generate root cert success, dir is %s' % dir)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)


def generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """
    try:
        ca = os.path.abspath(ca) 
        dir = os.path.abspath(dir) 
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/cts.sh gen_agency_cert ' + ca + ' ' + dir + ' ' + agent)
        if not status:
            logger.info(' Generate %s cert successful! dir is %s.'%(agent, dir + '/' + agent))
        else:
            consoler.error(' \033[1;31m Generate %s cert failed! Please check your network, and try to check your opennssl version.\033[0m')
            logger.error('  Generate %s cert failed! Result is %s'%(agent, result))
            raise MCError(' Generate %s cert failed! Result is %s'%(agent, result))
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result) 


def generator_node_ca(agent, dir, node):
    """[generate node cert ]
    
    Arguments:
        agent {[path]} -- [agency cert path]
        node {[string]} -- [node name]
        dir {[path]} -- [node cert path]
    """
    _dir = os.path.abspath(dir) 
    agent = os.path.abspath(agent) 
    try:
        (status, result)= utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/cts.sh gen_node_cert ' + agent + ' ' + _dir + '/ ' + node)
        if not status:
            logger.info(' Generate %s cert successful! dir is %s.', node, _dir + '/' + node)
        else:
            consoler.error(' \033[1;31m Generate node cert failed! Please check your network, and try to check your opennssl version.\033[0m')
            logger.error('  Generate %s cert failed! Result is %s'%(node, result))
            raise MCError(' Generate %s cert failed! Result is %s'%(node, result))
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)

def generator_sdk_ca(agency_dir,sdk_dir):
    """[generate sdkcert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """
    dir = os.path.abspath(agency_dir)
    sdk_dir = os.path.abspath(sdk_dir)
    try:
        (status, result)= utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/cts.sh gen_sdk_cert ' + dir + ' ' + sdk_dir)
        if not status:
            consoler.info(' Generate sdk cert successful! dir is %s.',  sdk_dir + '/sdk')
            logger.info(' Generate sdk cert successful! dir is %s.', sdk_dir + '/sdk')
        else:
            logger.error('  Generate sdk cert failed! Result is %s' %result)
            raise MCError(' Generate sdk cert failed! Result is %s' %result)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)


def gm_generate_root_ca(dir):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """
    try:
        dir = os.path.abspath(dir)
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/gm/cts.sh gen_chain_cert ' + dir)
        if status != 0:
            logger.warn(' cts.sh failed! status is %d, output is %s, dir is %s.', status, result, dir)
            raise MCError('cts.sh failed! status is %d, output is %s, dir is %s.' % (status, result, dir))
        logger.info(' cts.sh success! status is %d, output is %s, dir is %s.', status, result, dir)
        logger.info(' Generate root cert success, dir is %s', dir)
        consoler.info(' Generate root cert success, dir is %s' % dir)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)

def gm_generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """
    try:
        ca = os.path.abspath(ca) 
        dir = os.path.abspath(dir) 
        (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/gm/cts.sh gen_agency_cert ' + ca + ' ' + dir + ' ' + agent)
        if not status:
            logger.info(' Generate %s cert successful! dir is %s.'%(agent, dir + '/' + agent))
        else:
            consoler.error(' \033[1;31m Generate %s cert failed! Please check your network, and try to check your opennssl version.\033[0m')
            logger.error('  Generate %s cert failed! Result is %s'%(agent, result))
            raise MCError(' Generate %s cert failed! Result is %s'%(agent, result))
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result) 


def gm_generator_node_ca(agent, dir, node):
    """[generate node cert ]
    
    Arguments:
        agent {[path]} -- [agency cert path]
        node {[string]} -- [node name]
        dir {[path]} -- [node cert path]
    """
    _dir = os.path.abspath(dir) 
    agent = os.path.abspath(agent) 
    try:
        (status, result)= utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/gm/cts.sh gen_node_cert ' + agent + ' ' + _dir + '/ ' + node)
        if not status:
            logger.info(' Generate %s cert successful! dir is %s.', node, _dir + '/' + node)
        else:
            consoler.error(' \033[1;31m Generate node cert failed! Please check your network, and try to check your opennssl version.\033[0m')
            logger.error('  Generate %s cert failed! Result is %s'%(node, result))
            raise MCError(' Generate %s cert failed! Result is %s'%(node, result))
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)

def gm_generator_sdk_ca(agency_dir,sdk_dir):
    """[generate sdkcert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """
    dir = os.path.abspath(agency_dir)
    sdk_dir = os.path.abspath(sdk_dir)
    try:
        (status, result)= utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ca/gm/cts.sh gen_sdk_cert ' + dir + ' ' + sdk_dir)
        if not status:
            consoler.info(' Generate sdk cert successful! dir is %s.',  sdk_dir + '/sdk')
            logger.info(' Generate sdk cert successful! dir is %s.', sdk_dir + '/sdk')
        else:
            logger.error('  Generate sdk cert failed! Result is %s' %result)
            raise MCError(' Generate sdk cert failed! Result is %s' %result)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m Generate root cert failed! excepion is %s.\033[0m', e)
        logger.error('  Generate root cert failed! Result is %s'%result)

def check_cert_file(path):
    """[check node cert exist]
    
    Arguments:
        path {[dir -> node cert]} -- [where node cert put]
    
    Returns:
        [bool] -- [true or false]
    """

    result = os.path.exists(path + '/agency.crt') and os.path.exists(path + '/ca.crt')  and os.path.exists(path + '/node.key')\
        and os.path.exists(path + '/node.pubkey') and os.path.exists(path + '/node.crt')
    return result


def check_cert_sdk(path):
    """[check sdk cert exist]
    
    Arguments:
        path {[dir -> sdk cert]} -- [where sdk cert put]
    
    Raises:
        MCError -- [catch sdk Init status]
    
    Returns:
        [bool] -- [true or false]
    """

    result = os.path.exists(path + '/sdk/sdk.crt') and os.path.exists(path + '/sdk/ca.crt')  and os.path.exists(path + '/sdk/client.keystore')\
        and os.path.exists(path + '/sdk/keystore.p12') and os.path.exists(path + '/sdk/sdk.csr') and os.path.exists(path + '/sdk/sdk.key') and os.path.exists(path + '/sdk/sdk.param')\
        and os.path.exists(path + '/sdk/sdk.private') and os.path.exists(path + '/sdk/sdk.pubkey') 
    try:
        if result:
            consoler.info('  Init sdk cert success!')
        else:
            logger.error('  Init sdk cert failed!')
            raise MCError('  Init sdk cert failed!')
    except MCError as me:
        logger.error(me)
        consoler.error(me)
    return result    


def check_ca_exist(path):
    """[check root cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    result = os.path.exists(path + '/ca.crt') and os.path.exists(path + '/ca.key')
    return result

def check_gmca_exist(path):
    """[check root cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    result = os.path.exists(path + '/gmca.crt') and os.path.exists(path + '/gmca.key')
    return result


def check_agent_ca_exist(path):
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    result = os.path.exists(path + CA.agent + '/agency.crt') and os.path.exists(path + CA.agent + '/agency.key') and \
        os.path.exists(
            path + '/ca.crt') and os.path.exists(path + CA.agent + '/sdk')
    return result


def check_agent_gmca_exist(path):
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    result = os.path.exists(path + CA.agent + '/gmagency.crt') and os.path.exists(path + CA.agent + '/gmagency.key') and \
        os.path.exists(
            path + '/gmca.crt') and os.path.exists(path + CA.agent + '/sdk')
    return result


def init_ca(cert_path):
    """[init users' agenct ca]
    
    Arguments:
        cert_path {[dir]} -- [usrs' cert path]
    
    Raises:
        Exception -- [normal error]
    
    Returns:
        [bool] -- [true or flase]
    """

    if check_ca_exist(cert_path) and check_agent_ca_exist(cert_path):
        shutil.copytree(cert_path, get_ca_path())
        logger.info("Init cert, copy cert to cert_path")
    elif check_gmca_exist(cert_path) and check_agent_gmca_exist(cert_path):
        shutil.copytree(cert_path, get_GM_ca_path())
        logger.info("Init gm cert, copy gm cert to cert_path")
    else:
        logger.error("Init cert failed! files not completed")
        raise Exception("Init cert failed! files not completed")

    return 0








