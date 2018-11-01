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



def generate_root_ca(dir, chain = '12345'):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """
    try:
        int(chain)
    except Exception as e:
        logger.error('\033[1;31m  Generate root cert failed! Chain id must be (int), your chain id is %s.\033[0m',chain )
        raise Exception(' Generate root cert failed! Result is %s', e)
    sh_path =  path.get_path() + '/scripts/ca/'
     
    _dir = os.path.abspath(dir) 
    os.chdir(sh_path)
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_chain_cert ' + _dir + '/' + chain)
    os.chdir(path.get_path())
    if not status:
        logger.info(' Generate root cert successful! dir is %s.', _dir)
    else:
        logger.error('  Generate root cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate root cert failed! Result is %s', result)
        raise Exception(' Generate root cert failed! Result is %s', result)


def generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """

    ca = os.path.abspath(ca) 
    dir = os.path.abspath(dir) 
    sh_path =  path.get_path() + '/scripts/ca/'
    if os.path.exists(ca) and os.path.isfile(ca + '/ca.crt') and os.path.isfile(ca +  '/ca.key') and os.path.isfile(ca + '/cert.cnf'):
        logger.info('ca_path completed.')
    else:
        consoler.error(' \033[1;31m   Generate %s cert failed! Cant find cert in %s. \033[0m',agent, ca)
        raise Exception(' Generate %s cert failed! Cant find cert in %s. \033[0m',agent, ca)
    ca = path.get_path() + '/' + ca 
    os.chdir(sh_path)
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_agency_cert ' + ca + ' ' + dir + '/' + agent)
    os.chdir(path.get_path())
    if not status:
        logger.info(' Generate %s cert successful! dir is %s.', agent, dir + '/' + agent)
    else:
        logger.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate %s cert failed! Result is %s',agent, result)
        raise Exception(' Generate %s cert failed! Result is %s',agent, result)



def generator_node_ca(agent, dir, node):
    """[generate node cert ]
    
    Arguments:
        agent {[path]} -- [agency cert path]
        node {[string]} -- [node name]
        dir {[path]} -- [node cert path]
    """
    sh_path =  path.get_path() + '/scripts/ca/'
    _dir = os.path.abspath(dir) 
    agent = os.path.abspath(agent) 
    try:
        get_agent = agent.split('/')
        agent_name = get_agent[len(get_agent)-1]
    except Exception as e:
        consoler.error(' \033[1;31m   Generate %s cert failed! %s. \033[0m',agent_name, e)
        raise Exception(' Generate %s cert failed! %s.',agent_name, e)
    if os.path.exists(agent) and os.path.isfile(agent +  '/agency.crt') and os.path.isfile(agent + '/agency.key'):
        try:
            os.chdir(sh_path)
            (status, result)= utils.getstatusoutput('./cert_tools.sh gen_node_cert ' + agent + ' ' + _dir + '/' + node)
            os.chdir(path.get_path())
        except Exception as e:
            logger.error('  Generate %s cert failed! %s.',agent_name, e)
            raise Exception(' Generate %s cert failed! %s.',agent_name, e)
    else:
        logger.error('  Generate %s cert failed! Cant find %s.',agent_name, agent)
        raise Exception(' Generate %s cert failed! Cant find %s.',agent_name, agent)
    if not status:
        logger.info(' Generate %s cert successful! dir is %s.', node, _dir + '/' + node)
    else:
        logger.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate %s cert failed! Result is %s',node, result)
        raise Exception(' Generate %s cert failed! Result is %s',node, result)

def generator_sdk_ca(agency_dir,sdk_dir):
    """[generate sdkcert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """
    dir = os.path.abspath(agency_dir)
    sdk_dir = os.path.abspath(sdk_dir)
    sh_path =  path.get_path() + '/scripts/ca/'
    if os.path.exists(dir) and os.path.isfile(dir +  '/agency.crt') and os.path.isfile(dir + '/agency.key'):
        try:
            get_agent = dir.split('/')
            agent_name = get_agent[len(get_agent)-1]
            logger.debug("name is "+agent_name)
            os.chdir(sh_path)
            (status, result)= utils.getstatusoutput('./cert_tools.sh  gen_sdk_cert ' + dir + ' ' + sdk_dir + '/sdk')
            os.chdir(path.get_path())
        except Exception as e:
            logger.error('  Copy %s cert failed! %s.',agent_name, e)
            raise Exception(' Copy %s cert failed! %s.',agent_name, e)
            
    else:
        logger.error('  Copy %s cert failed! %s.',agent_name, e)
        raise Exception(' Copy %s cert failed! %s.',agent_name, e)

    if not status:
        consoler.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
        logger.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
    else:
        logger.error('  Generate sdk cert failed! Result is %s', result)
        raise Exception(' Generate sdk cert failed! Result is %s', result)


def gm_generate_root_ca(dir, chain = '12345'):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """


    sh_path =  path.get_path() + '/scripts/ca/'
    temp_path = path.get_path() + '/cert_temp'
    shutil.copytree(sh_path, temp_path)
    os.chdir(path.get_path() + '/cert_temp/gm')
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_chain_cert ' + chain)
    os.chdir(path.get_path())
    if not os.path.exists(dir + '/' + chain):
        os.makedirs(dir + '/' + chain)
    if not status:
        try:
            shutil.copy(temp_path + '/gm/gmca.crt', dir + '/' + chain)
            shutil.copy(temp_path + '/gm/gmca.key', dir + '/' + chain)
            shutil.copy(temp_path + '/gm/gmsm2.param', dir + '/' + chain)
            shutil.copy(temp_path + '/gm/cert.cnf', dir + '/' + chain)
            logger.info(' Generate root cert successful! dir is %s.', dir + '/' + chain)
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error('  Generate root cert failed! %s.',e)
            raise Exception(' Generate root cert failed! %s.',e)
    else:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        logger.error('  Generate root cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate root cert failed! Result is %s', result)
        raise Exception(' Generate root cert failed! Result is %s', result)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


def gm_generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """


    sh_path =  path.get_path() + '/scripts/ca/'
    temp_path = path.get_path() + '/cert_temp'
    shutil.copytree(sh_path, temp_path)
    if os.path.exists(ca) and os.path.isfile(ca + '/gmca.crt') and os.path.isfile(ca +  '/gmca.key') and os.path.isfile(ca + '/cert.cnf'):
        shutil.copy(ca + '/gmca.crt', temp_path + '/gm/')
        shutil.copy(ca + '/gmca.key', temp_path + '/gm/')
        shutil.copy(ca + '/gmsm2.param', temp_path + '/gm/')
    else:
        consoler.error(' \033[1;31m   Generate %s cert failed! Cant find cert in %s. \033[0m',agent, ca)
        logger.error(' Generate %s cert failed! Cant find cert in %s. \033[0m',agent, ca)
    os.chdir(path.get_path() + '/cert_temp/gm')
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_agency_cert ' + agent)
    os.chdir(path.get_path())
    if not status:
        try: 
            os.mkdir(dir + '/' + agent)
            shutil.copy(temp_path + '/gm/' + agent + '/gmagency.crt', dir + '/' + agent)
            shutil.copy(temp_path + '/gm/' + agent + '/gmagency.key', dir + '/' + agent)
            shutil.copy(temp_path + '/gm/' + agent + '/gmsm2.param', dir + '/' + agent)
            shutil.copy(temp_path + '/gm/' + agent + '/gmca.crt', dir + '/' + agent)
            shutil.copy(temp_path + '/gm/' + agent + '/cert.cnf', dir + '/' + agent)
            logger.info(' Generate %s cert successful! dir is %s.', agent, dir + '/' + agent)
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error('  Generate %s cert failed! %s.',agent, e)
            raise Exception(' Generate %s cert failed! %s.',agent, e)
    else:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        logger.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate %s cert failed! Result is %s',agent, result)
        raise Exception(' Generate %s cert failed! Result is %s',agent, result)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)



def gm_generator_node_ca(agent, dir, node):
    """[generate node cert ]
    
    Arguments:
        dir {[path]} -- [node cert path]
        node {[string]} -- [node name]
        agent {[path]} -- [agency cert path]
    """
    sh_path =  path.get_path() + '/scripts/ca/'
    temp_path = path.get_path() + '/cert_temp'
    shutil.copytree(sh_path, temp_path)
    try:
        get_agent = agent.split('/')
        agent_name = get_agent[len(get_agent)-1]
    except Exception as e:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        consoler.error(' \033[1;31m   Generate %s cert failed! %s. \033[0m',agent_name, e)
        raise Exception(' Generate %s cert failed! %s.',agent_name, e)
    if os.path.exists(agent) and os.path.isfile(agent +  '/gmagency.crt') and os.path.isfile(agent + '/gmagency.key'):
        try:
            shutil.copytree(agent, temp_path + '/gm/' + agent_name)
            os.chdir(path.get_path() + '/cert_temp/gm')
            (status, result)= utils.getstatusoutput('./cert_tools.sh gen_node_cert ' + agent_name + ' ' + node)
            os.chdir(path.get_path())
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error('  Generate %s cert failed! %s.',agent_name, e)
            raise Exception(' Generate %s cert failed! %s.',agent_name, e)
    else:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        logger.error('  Generate %s cert failed! Cant find %s.',agent_name, agent)
        raise Exception(' Generate %s cert failed! Cant find %s.',agent_name, agent)
    if not status:
        try:
            os.mkdir(dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmagency.crt', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmca.crt', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmennode.crt', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmennode.key', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.ca', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.crt', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.json', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.key', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.nodeid', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.private', dir + '/' + node)
            shutil.copy(temp_path + '/gm/' + agent_name + '/' + node + '/gmnode.serial', dir + '/' + node)
            logger.info(' Generate %s cert successful! dir is %s.', node, dir + '/' + node)
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error('  Generate %s cert failed! %s.',node, e)
            raise Exception(' Generate %s cert failed! %s.',node, e)
    else:
        logger.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate %s cert failed! Result is %s',node, result)
        raise Exception(' Generate %s cert failed! Result is %s',node, result)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

def gm_generator_sdk_ca(agency_dir,sdk_dir):
    """[generate sdkcert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """
    dir = agency_dir
    sh_path =  path.get_path() + '/scripts/ca/'
    temp_path = path.get_path() + '/cert_temp'
    shutil.copytree(sh_path, temp_path)
    if os.path.exists(dir) and os.path.isfile(dir +  '/gmagency.crt') and os.path.isfile(dir + '/gmagency.key'):
        try:
            get_agent = dir.split('/')
            agent_name = get_agent[len(get_agent)-1]
            shutil.copytree(dir, temp_path +  '/gm/' +agent_name)
            logger.debug("name is "+agent_name)
            os.chdir(path.get_path() + '/cert_temp/gm')
            (status, result)= utils.getstatusoutput('./cert_tools.sh  gen_sdk_cert ' + agent_name + ' sdk')
            os.chdir(path.get_path())
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error('  Copy %s cert failed! %s.',agent_name, e)
            raise Exception(' Copy %s cert failed! %s.',agent_name, e)
            
    else:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        logger.error('  Copy %s cert failed! %s.',agent_name, e)
        raise Exception(' Copy %s cert failed! %s.',agent_name, e)

    if not status:
        try:
            shutil.copytree(temp_path + '/gm/' + agent_name + '/sdk', sdk_dir + '/sdk')
            consoler.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
            logger.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error(' Generate sdk cert failed! dir is %s/sdk.', sdk_dir)
            raise Exception(' Generate sdk cert failed! dir is %s/sdk.', sdk_dir)
    else:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        logger.error('  Generate sdk cert failed! Result is %s', result)
        raise Exception(' Generate sdk cert failed! Result is %s', result)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


def check_cert_complete(cc, cert_path):
    """[check node cert]
    
    Arguments:
        cc {[config]} -- [config.conf, e.g.sample_12345_v1.0.conf]
        cert_path {[dir]} -- [where save cert in]
    
    Returns:
        [bool] -- [true or false]
    """

    cf = configparser.ConfigParser()
    cf.read('./conf/mchain.conf')
    agency = cf.get('agent','agent_name')
    try:
        chain_id = cc.get_chain().get_id()
        chain_version = cc.get_chain().get_version()
        for node in cc.get_nodes():
            for index in range(0, node.get_node_num()):
                consoler.info(' chain:%s, version:%s, host_ip:%s, index %s .',chain_id ,chain_version, node.get_host_ip(), index)
                check_path = cert_path[0] + '/' + str(chain_id) + '/' + str(chain_version) + '/' + str(node.get_host_ip()) + '/node' + str(index)
                if check_cert_file(check_path):
                    (status, result)= utils.getstatusoutput('bash' + ' ./scripts/ca/cert_generate.sh ' + check_path + ' ' + agency)
                    if not status:
                        consoler.info('  Init cert success! %s.',result)
                    else:
                        raise Exception('Init cert failed, %s.',result)
                else:
                    raise Exception('cant find cert in %s.', check_path)
    except Exception as e:
        logger.error(e)
        raise Exception(' \t %s', e)
    return 0


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
    os.path.exists(path + '/ca.crt') and os.path.exists(path + CA.agent + '/sdk')
    return result

def check_agent_gmca_exist(path):
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    result = os.path.exists(path + CA.agent + '/gmagency.crt') and os.path.exists(path + CA.agent + '/gmagency.key') and \
    os.path.exists(path + '/gmca.crt') and os.path.exists(path + CA.agent + '/sdk')
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

def installgm():
    os.chdir(path.get_path() + '/cert_temp/gm')
    gmpath = os.path.abspath('./') 
    (status, result) = utils.getstatusoutput('./install_tassl.sh ' + gmpath)
    old = 'OPENSSL_CMD=/mnt/c/Users/asherli/Desktop/ca/bin/openssl'
    new = gmpath + '/bin/openssl'
    utils.replace('./cert_tools.sh',old,new)
    os.chdir(path.get_path())
    if not status:
        logger.info(' Init gm cert successful!')
    else:
        consoler.error(' \033[1;31m  Init gm cert failed \033[0m')
        logger.error('  Init gm cert failed')
        raise Exception(' Init gm cert failed! Result is %s', result) 








