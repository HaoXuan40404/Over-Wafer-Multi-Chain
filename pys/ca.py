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

    return CA.CA_path + '/' + '/NA' + CA.agent

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

    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    (status, result) = utils.getstatusoutput('bash $scripts/generate_chain_cert.sh -o $out')
    if not status:
        logger.info(' Generate root cert successful! dir is %s.', dir)
    else:
        consoler.error('  Generate root cert failed! Please check your network, and try to check your opennssl version.')
        consoler.error('  Generate root cert failed! Result is %s', result)
        logger.error(' Generate root cert failed! Result is %s', result)


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
    (status, result)= utils.getstatusoutput('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent')
    if not status:
        logger.info(' Generate %s cert successful! dir is %s.', agent, dir)
    else:
        consoler.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        consoler.error('  Generate %s cert failed! Result is %s',agent, result)
        logger.error(' Generate %s cert failed! Result is %s',agent, result)



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
    (status, result)= utils.getstatusoutput('bash $scripts/generate_node_cert.sh -a $agent -d $agent -n $node -o $out')
    if not status:
        logger.info(' Generate %s cert successful! dir is %s.', node, dir)
    else:
        consoler.error('  Generate %s cert failed! Please check your network, and try to check your opennssl version.')
        consoler.error('  Generate %s cert failed! Result is %s',node, result)
        logger.error(' Generate %s cert failed! Result is %s',node, result)

def generator_sdk_ca(dir):
    """[generate sdkcert ]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """

    os.environ['out'] = dir
    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    (status, result)= utils.getstatusoutput('bash $scripts/generate_sdk_cert.sh -d $out')
    if not  status:
        logger.info(' Generate sdk cert successful! dir is %s/sdk.', dir)
    else:
        logger.error('  Generate sdk cert failed! Please check your network, and try to check your opennssl version.')
        logger.error(' Generate sdk cert failed! Result is %s', result)
        raise Exception('  Generate sdk cert failed! Result is %s', result)
        
    return 0

def gm_generate_root_ca(dir):
    """[generate guomi root cert]
    
    Arguments:
        dir {[dir]} -- [put ca in dir]
    """
    
    os.environ['scripts'] = path.get_path() + '/scripts/ca/'
    os.environ['out'] = dir
    (status, result)= utils.getstatusoutput('bash $scripts/generate_chain_cert.sh -o $out -g')
    if not status:
        logger.info(' Generate GM root cert successful! dir is %s.', dir)
    else:
        logger.error('  Generate GM root cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate GM root cert failed! Result is %s', result)
        raise Exception(' Generate GM root cert failed! Result is %s', result)

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
    (status, result)= utils.getstatusoutput('bash $scripts/generate_agency_cert.sh -c $ca -o $out -n $agent -g')
    if not status:
        logger.info(' Generate GM %s cert successful! dir is %s.', agent, dir)
    else:
        logger.error('  Generate GM %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate GM %s cert failed! Result is %s',agent, result)
        raise Exception(' Generate GM %s cert failed! Result is %s',agent, result)

def gm_generator_node_ca(agent,dir, node):
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
    (status, result)= utils.getstatusoutput('bash $scripts/generate_node_cert.sh -a WB -d $agent -n $node -o $out -s sdk -g')
    if not status:
        logger.info(' Generate GM %s cert successful! dir is %s.', node, dir)
    else:
        logger.error('  Generate GM %s cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate GM %s cert failed! Result is %s',node, result)
        raise Exception(' Generate GM %s cert failed! Result is %s',node, result)





def new_generate_root_ca(dir, chain = '12345'):
    """[generate root cert]
    
    Arguments:
        dir {[path]} -- [root cert path]
    """


    sh_path =  path.get_path() + '/scripts/ca/'
    temp_path = path.get_path() + '/cert_temp'
    os.mkdir(path.get_path() + '/cert_temp')
    shutil.copy(sh_path + '/cert_tools.sh', temp_path)
    shutil.copy(sh_path + '/cert.cnf', temp_path)
    os.chdir(path.get_path() + '/cert_temp')
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_chain_cert ' + chain)
    os.chdir(path.get_path())
    if not status:
        try:
            shutil.copy(temp_path + '/ca.crt', dir)
            shutil.copy(temp_path + '/ca.key', dir)
            shutil.copy(temp_path + '/cert.cnf', dir)
            logger.info(' Generate root cert successful! dir is %s.', dir)
        except Exception as e:
            logger.error('  Generate root cert failed! %s.',e)
            raise Exception(' Generate root cert failed! %s.',e)
    else:
        logger.error('  Generate root cert failed! Please check your network, and try to check your opennssl version.')
        logger.error('  Generate root cert failed! Result is %s', result)
        raise Exception(' Generate root cert failed! Result is %s', result)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


def new_generator_agent_ca(dir, ca, agent):
    """[generate agency cert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        ca {[path]} -- [root cert path]
        agent {[string]} -- [agency name]
    """


    sh_path =  path.get_path() + '/scripts/ca/'
    os.mkdir(path.get_path() + '/cert_temp')
    temp_path = path.get_path() + '/cert_temp'
    if os.path.exists(ca) and os.path.isfile(ca + '/ca.crt') and os.path.isfile(ca +  '/ca.key') and os.path.isfile(ca + '/cert.cnf'):
        shutil.copy(ca + '/ca.crt', temp_path)
        shutil.copy(ca + '/ca.key', temp_path)
        shutil.copy(ca + '/cert.cnf', temp_path)
    else:
        consoler.error('  Generate %s cert failed! Cant find cert in %s.',agent, ca)
        logger.error(' Generate %s cert failed! Cant find cert in %s.',agent, ca)
    os.chdir(path.get_path() + '/cert_temp')
    shutil.copy(sh_path + '/cert_tools.sh', temp_path)
    shutil.copy(sh_path + '/cert.cnf', temp_path)
    (status, result) = utils.getstatusoutput('./cert_tools.sh gen_agency_cert ' + agent)
    os.chdir(path.get_path())
    if not status:
        try: 
            os.mkdir(dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/agency.crt', dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/agency.csr', dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/agency.key', dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/ca-agency.crt', dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/ca.crt', dir + '/' + agent)
            shutil.copy(temp_path + '/' + agent + '/cert.cnf', dir + '/' + agent)
            logger.info(' Generate %s cert successful! dir is %s.', agent, dir + '/' + agent)
            raise Exception(' Generate %s cert successful! dir is %s.', agent, dir + '/' + agent)
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



def new_generator_node_ca(agent, dir, node):
    """[generate node cert ]
    
    Arguments:
        dir {[path]} -- [node cert path]
        node {[string]} -- [node name]
        agent {[path]} -- [agency cert path]
    """
    sh_path =  path.get_path() + '/scripts/ca/'
    os.mkdir(path.get_path() + '/cert_temp')
    temp_path = path.get_path() + '/cert_temp'
    try:
        get_agent = agent.split('/')
        agent_name = get_agent[len(get_agent)-1]
    except Exception as e:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        consoler.error('  Generate %s cert failed! %s.',agent_name, e)
        raise Exception(' Generate %s cert failed! %s.',agent_name, e)
    if os.path.exists(agent) and os.path.isfile(agent +  '/agency.crt') and os.path.isfile(agent + '/agency.key'):
        try:
            shutil.copytree(agent, temp_path + '/' + agent_name)
            os.chdir(path.get_path() + '/cert_temp')
            shutil.copy(sh_path + '/cert_tools.sh', temp_path)
            shutil.copy(sh_path + '/cert.cnf', temp_path)
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
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/agency.crt', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/ca.crt', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.ca', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.crt', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.csr', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.json', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.key', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.nodeid', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.param', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.private', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.pubkey', dir + '/')
            shutil.copy(temp_path + '/' + agent_name + '/' + node + '/node.serial', dir + '/')
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

def new_generator_sdk_ca(agency_dir,sdk_dir):
    """[generate sdkcert]
    
    Arguments:
        dir {[path]} -- [agency cert path]
        If operation success, dir will generate sdk dir under the target path, the content is sdk_cert.
    """
    dir = agency_dir
    sh_path =  path.get_path() + '/scripts/ca/'
    os.mkdir(path.get_path() + '/cert_temp')
    temp_path = path.get_path() + '/cert_temp'
    if os.path.exists(dir) and os.path.isfile(dir +  '/agency.crt') and os.path.isfile(dir + '/agency.key'):
        try:
            get_agent = dir.split('/')
            agent_name = get_agent[len(get_agent)-1]
            shutil.copytree(dir, temp_path +  '/' +agent_name)
            logger.debug("name is "+agent_name)
            shutil.copy(sh_path + '/cert_tools.sh', temp_path)
            shutil.copy(sh_path + '/cert.cnf', temp_path)
            os.chdir(path.get_path() + '/cert_temp')
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
            shutil.copytree(temp_path + '/' + agent_name + '/sdk', sdk_dir + '/sdk')
            consoler.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
            logger.info(' Generate %s cert successful! dir is %s.', agent_name, sdk_dir + '/sdk')
        except Exception as e:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            logger.error(' Generate sdk cert failed! dir is %s/sdk.', sdk_dir)
            raise Exception(' Generate sdk cert failed! dir is %s/sdk.', sdk_dir)
    else:
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
    
    return (path + '/ca.crt') and (path + '/ca.key')

def check_gmca_exist(path):
    """[check root cert exists]
    
    Returns:
        [bool] -- [true or false]
    """
    
    return (path + '/gmca.crt') and (path + '/gmca.key')

def check_agent_ca_exist(path):
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """

    return (path + '/'+ CA.agent + '/agency.crt') and (path + '/'+ CA.agent + '/agency.key')

def check_agent_gmca_exist(path):
    """[check agency cert exists]
    
    Returns:
        [bool] -- [true or false]
    """

    return (path + '/'+ CA.agent + '/gmagency.crt') and (path + '/'+ CA.agent + '/gmagency.key')



def init_ca(cert_path):
    if check_ca_exist(cert_path) and check_agent_ca_exist(cert_path):
        shutil.copytree(cert_path, get_ca_path() +  '/' + CA.agent)
        logger.info("Init cert, copy cert to cert_path")
    elif check_gmca_exist(cert_path) and check_agent_gmca_exist(cert_path):
        shutil.copytree(cert_path, get_GM_ca_path() +  '/' + CA.agent)
        logger.info("Init gm cert, copy gm cert to cert_path")
    else:
        logger.error("Init cert failed! files not completed")
        raise Exception("Init cert failed! files not completed")

    return 0






