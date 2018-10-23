#coding:utf-8
import os
import json
import shutil
from pys import path
from pys import ansible, utils
from pys.chain.meta import *
from pys.chain.package import AllChain
from pys.chain.package import ChainVers
from pys.chain.package import VerHosts
from pys.chain.package import HostNodeDirs
from pys.chain.port import AllChainPort
from pys.chain.port import HostPort
from pys.log import logger
from pys.log import consoler
from pys.chain import data
from pys.chain import package

def init_chain():
    """[init]
    """

    os.system('sudo bash ./scripts/hostsname.sh')
    os.system('bash ./scripts/ssh_copy_add.sh')


def start_chain(chain):
    """[start nodes]
    
    Arguments:
        chain {[list]} -- [get chain_id:host_ip from command Line]
    """

    if chain[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                start_server(chain_id)
        else:
            consoler.info(' No published chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_chain_id(chain_get[0]):
                    start_server(chain_get[0])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s', chain_get[0])
            elif len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    if utils.valid_ip(chain_get[1]):
                        ansible.start_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                    else:
                        consoler.info(' skip, invalid host, chain_id is %s, host is %s', chain_get[0], chain_get[1])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s, host is %s', chain_get[0], chain_get[1])
            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)


def stop_chain(chain):
    """[stop nodes]
    
    Arguments:
        chain {[list]} -- [get chain_id:host_ip from command Line]
    """

    if chain[0] == 'all':
        consoler.info('You want to stop all node,are you sure? yes or no? y/n')
        choice = raw_input('Your choice is: ')
        if ((choice == 'yes') | (choice == 'Yes') | (choice == 'Y') | (choice == 'y')):
            dir = data.meta_dir_base()
            if os.path.exists(dir):
                for chain_id in os.listdir(dir):
                    stop_server(chain_id)
            else:
                consoler.info(' No published chain exist, do nothing.')
        else:
            consoler.info(' input No, and will do nothing.')
            logger.info('refuse stop all node')
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_chain_id(chain_get[0]):
                    stop_server(chain_get[0])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s', chain_get[0])
            elif len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    if utils.valid_ip(chain_get[1]):
                        ansible.stop_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                    else:
                        consoler.info(' skip, invalid host, chain_id is %s, host is %s', chain_get[0], chain_get[1])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s, host is %s', chain_get[0], chain_get[1])
            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)

def check_chain(chain):
    """[Check if the nodes is running normally.]
    
    Arguments:
        chain {[list]} -- [get chain_id:host_ip from command Line]
    """
    
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                check_server(chain_id)
        else:
            consoler.info(' No published chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_chain_id(chain_get[0]):
                    check_server(chain_get[0])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s', chain_get[0])
            elif len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    if utils.valid_ip(chain_get[1]):
                        ansible.check_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                    else:
                        consoler.info(' skip, invalid host, chain_id is %s, host is %s', chain_get[0], chain_get[1])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s, host is %s', chain_get[0], chain_get[1])

            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)

def env_check(hosts):
    """[check and confirm the environment normally]
    
    Arguments:
        hosts {string} -- host list
    """
    if hosts[0] == 'all':
        ansible.env_check('all', path.get_path())
    else:
        for host in hosts:
            if utils.valid_ip(host):
                ansible.env_check(host, path.get_path())
            else:
                consoler.log(' skip, not invalid host, host is %s', host)

def monitor_chain(chain):
    """[Check the chain's parameters e.g. blocknumber, consensus list...etc]
    
    Arguments:
        chain {[list]} -- [get chain_id:host_ip from command Line]
    """
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                monitor_server(chain_id)
        else:
            consoler.info(' No published chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_chain_id(chain_get[0]):
                    monitor_server(chain_get[0])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s', chain_get[0])
            elif len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    if utils.valid_ip(chain_get[1]):
                        ansible.monitor_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                    else:
                        consoler.info(' skip, invalid host, chain_id is %s, host is %s', chain_get[0], chain_get[1])
                else:
                    consoler.info(' skip, invalid chain_id, chain_id is %s, host is %s', chain_get[0], chain_get[1])
            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)

def pub_list(chains):
    """[List the nodes in package corresponding to the --publishi chain:version]
    
    Arguments:
        chains {[list]} -- [chain id]
    """

    logger.info('list begin, chains is %s', chains)
    consoler.info(' chains is %s' % chains)

    meta_list = []
    if chains[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                m = Meta(chain_id)
                if not m.empty():
                    meta_list.append(m)
        else:
            consoler.info(' No published chain exist, do nothing.')
    else:
        for chain_id in chains:
            m = Meta(chain_id)
            if not m.empty():
                meta_list.append(m)

    for m in meta_list:
        consoler.info(' => chain id ： %s' % m.get_chain_id())
        nodes = m.get_nodes()
        for node in nodes.iterkeys():
            consoler.info('\t host => %s' % node)

    logger.info('list end.')

def pkg_list(chains):
    """list all version and all pacakge of the chain
    
    Arguments:
        chains {[type]} -- all chains
    """

    logger.info(' chains is %s', chains)

    consoler.info(' chains is %s' % chains)

    if chains[0] == 'all':
        ac = AllChain()
        chains = ac.get_chains()
        if len(chains) == 0:
            consoler.info(' No build chain exist, do nothing.')
        
    for chain in chains:
        logger.debug(' chain id is %s', chain)
        consoler.info(' ==> chain id ： %s', chain)
        cv = ChainVers(chain)
        if len(cv.get_ver_list()) == 0:
            consoler.info(' No build version exist for chain %s, do nothing.', chain)

        for version in cv.get_ver_list():
            consoler.info('\t\t => chain version ： %s', version)
            logger.debug(' chain id is %s, chain version is %s', chain, version)
            vh = VerHosts(chain, version)
            for pkg in vh.get_pkg_list():
                consoler.info('\t\t\t => package ：%s', pkg)
                hn = HostNodeDirs(chain, version, pkg)
                hp = HostPort(chain, version, pkg)
                for node_dir in hn.get_node_dirs():
                    consoler.info('\t\t\t\t => %s %s', node_dir, hp.get_by_index(node_dir))

    logger.info('load end')

def telnet_ansible(server):
    """[Test ansible operation to all server in operation server]
    
    Arguments:
        server {[list]} -- [host ip]
    """

    if server[0] == 'all':
        ansible.telnet_module('all')
    else:
        for i in range(len(server)):
            if utils.valid_ip(server[i]):
                ansible.telnet_module(server[i])
            else:
                consoler.error('skip host %s, invalid host format.', server[i])

def valid_cmd(chain):
    """[Determine if the cmd is valid or not
        chain:version]
    
    Arguments:
        chain {[string]} -- [chain cmd]
    
    Returns:
        [chain] -- [if valid return chainlist[]，else return false]
    """

    try: 
        chain_get = chain.split(':')
        chain_get[1]
        return chain_get
    except Exception as e:
        logger.error('%s is not a valid cmd', e)
        return False

def valid_file(chain):
    """[Determine if the cmd is exist
        chain:version:hostip]
    
    Arguments:
        chain {[string]} -- [chain cmd]
    
    Returns:
        [chain] -- [if valid return chainlist[]，else return false]
    """

    try: 
        chain_get = chain.split(':')
        chain_get[2]
        return chain_get
    except Exception as e:
        logger.error('%s is not a valid cmd', e)
        return False

def cmd_push(chain):
    """[Execute commands on multi servers]
    
    Arguments:
        chain {[list]} -- [chain_id:"cmd using":"split chain and cmd，e.g."chain:"cmd. 
        using '\"' includes command  e.g. "cmd1 cmd2"]
    """

    if valid_cmd(chain[0])[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                cmd_server(chain_id,valid_cmd(chain[0])[1])
        else:
            consoler.info(' No input chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = valid_cmd(chain[i])
            if len(chain_get) == 2:
                if utils.valid_chain_id(chain_get[0]):
                    cmd_server(chain_get[0],chain_get[1])
                elif utils.valid_ip(chain_get[0]):
                    ansible.cmd_module(chain_get[0],chain_get[1])
                else:
                    consoler.info(' skip, invalid cmd, cmd is %s %s', chain_get[0], chain_get[1])
            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)

def cmd_server(chain_id, cmd):
    """[Execute commands on a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)

    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not cmd action, chain_id is %s', chain_id)
        return 

    logger.info('cmd action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.cmd_module(k, cmd)


def file_push(chain):
    """[Push files on muti servers]
    
    Arguments:
        chain {[list]} -- [chain_id:src:dest using":"split.]
    """

    if valid_file(chain[0])[0] == 'all':
        dir = data.meta_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                file_server(chain_id,valid_file(chain[0])[1], valid_file(chain[0])[2])
        else:
            consoler.info(' No input chain exist, do nothing.')
    else:
        for i in range(len(chain)):
            chain_get = valid_file(chain[i])
            if len(chain_get) == 3:
                if utils.valid_chain_id(chain_get[0]):
                    file_server(chain_get[0],chain_get[1],chain_get[2])
                elif utils.valid_ip(chain_get[0]):
                    ansible.copy_module(chain_get[0],chain_get[1],chain_get[2])
                else:
                    consoler.info(' skip, invalid file_push, file_push is %s %s %s ', chain_get[0], chain_get[1], chain_get[2])
            else:
                consoler.info(' skip, invalid format, not chain_id:host, input %s', chain_get)


def file_server(chain_id, src, dest):
    """[Push files on a chain]
    
    Arguments:
        chain_id {[string]} -- [push files on all servers of a chain]
    """

    mm = Meta(chain_id)

    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not cmd action, chain_id is %s', chain_id)
        return 

    logger.info('cmd action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.copy_module(k, src, dest)


def start_server(chain_id):
    """[Using start.sh start all nodes of a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not start action, chain_id is %s', chain_id)
        return 

    logger.info('start action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.start_module(k, ansible.get_dir() + '/' + chain_id)





def stop_server(chain_id):
    """[Using stop.sh stop all nodes of a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)

    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not stop action, chain_id is %s', chain_id)
        return 

    logger.info('stop action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.stop_module(k, ansible.get_dir() + '/' + chain_id)


def check_server(chain_id):
    """[Using scheck.sh check all nodes of a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not check action, chain_id is %s', chain_id)
        return 

    logger.info('check action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)


def monitor_server(chain_id):
    """[Using monitor.sh check all nodes of a chain]
    
    Arguments:
        chain_id {[string]} -- [chain_id:version]
    """

    mm = Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not monitor action, chain_id is %s', chain_id)
        return 

    logger.info('monitor_server action, chain_id is ' + chain_id)
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.monitor_module(k, ansible.get_dir() + '/' + chain_id)

def export_package(export_list, dest):
    """[export package into dest]
    
    Arguments:
        export_list {[list]} -- [chain_id:version]
        dest {[mkdir]} -- [destination]
    """

    chain_get = valid_cmd(export_list)
    
    if utils.valid_chain_id(chain_get[0]):
        dir = data.package_dir(chain_get[0], chain_get[1])
        for host in os.listdir(dir):
            if utils.valid_ip(host):
                shutil.copytree(dir + '/' + host, dest + '/' + host)
                shutil.copytree(dir + '/common', dest + '/' + host + '/common')
            else:
                logger.debug('not invalid host_ip ' + host)    
    else:
        consoler.error('invalid chain_id format. %s %s', chain_get[0], chain_get[1])

def ls_port(hosts):
    """[show in host_ip which port used (published fisco-bcos) ]
    
    Arguments:
        hosts {[string]} -- [host_ip]
    """

    am = AllMeta()

    for host in hosts:
        consoler.info(' => host is %s', host)
        if not utils.valid_ip(host):
            consoler.info(' \t => Invalid host ip, host is %s.', host)
            continue
        
        metas = get_meta_ports_by_host(host, am)
        if len(metas) == 0:
            consoler.info(' \t => No chain published to this host.')
            continue
        
        for meta in metas:
            consoler.info(' \t => chain id is %s ', meta.get_chain_id())
            nodes = meta.get_host_nodes(host)
            for node in nodes:
                consoler.info(' \t\t node%s, rpc_port：%s, p2p_port：%s, channel_port：%s', str(node.get_index()), str(node.get_rpc()), str(node.get_p2p()), str(node.get_channel()))


   