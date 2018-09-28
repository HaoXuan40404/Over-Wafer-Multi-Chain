#coding:utf-8
import os

from pys import ansible, utils
from pys.chain import meta
from pys.chain.meta import Meta
from pys.chain.package import Package
from pys.log import logger
from pys.log import consoler
from pys.chain import data
from pys.chain import package


def start_chain(chain):
    """[解析命令行, 批量启动节点]
    
    Arguments:
        chain {[list]} -- [命令行传入的chain_id:host_ip]
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
    """[解析命令行, 批量停止节点]
    
    Arguments:
        chain {[list]} -- [命令行传入的chain_id:host_ip]
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
    """[解析命令行, 批量检查节点启动情况]
    
    Arguments:
        chain {[list]} -- [命令行传入的chain_id:host_ip]
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
    """依赖检查
    
    Arguments:
        hosts {string} -- host列表
    """
    if hosts[0] == 'all':
        ansible.env_check('all', ansible.get_dir())
    else:
        for host in hosts:
            if utils.valid_ip(host):
                ansible.env_check(host, ansible.get_dir())
            else:
                consoler.log(' skip, not invalid host, host is %s', host)

def monitor_chain(chain):
    """[解析命令行, 批量检查节点运行情况]
    
    Arguments:
        chain {[list]} -- [命令行传入的chain_id:host_ip]
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
    """[列出部署后链的安装包对应的节点]
    
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
                m.load_from_file()
                meta_list.append(m)
        else:
            consoler.info(' No published chain pkg exist, do nothing.')
    else:
        for chain_id in chains:
            m = Meta(chain_id)
            m.load_from_file()
            meta_list.append(m)

    for m in meta_list:
        consoler.info(' => chain is %s' % m.get_chain_id())
        nodes = m.get_nodes()
        for node in nodes.itervalues():
            consoler.info('\t node => %s' % node)

    logger.info('list end.')

def pkg_list(chains, host_detail = True):
    """[列出生成链的安装包对应的节点]
    
    Arguments:
        chains {[list]} -- [chain id]
    
    Keyword Arguments:
        host_detail {bool} -- [description] (default: {True})
    """


    logger.info('chains is %s, host_detail is %s', chains, host_detail)

    consoler.info(' chains is %s' % chains)

    pkg_list = []
    if chains[0] == "all":
        dir = data.package_dir_base()
        if os.path.exists(dir):
            for chain_id in os.listdir(dir):
                p = Package(chain_id)
                p.load()
                pkg_list.append(p)
        else:
            consoler.info(' No build chain pkg exist, do nothing.')
    else:
        for chain_id in chains:
            p = Package(chain_id)
            p.load()
            pkg_list.append(p)

    for p in pkg_list:
        consoler.info(' => chain is %s' % p.get_chain_id())
        for v in p.get_version_list():
            consoler.info(' \t version is %s' % v.get_chain_version())
            if isinstance(host_detail, bool) and host_detail:
                for h in v.get_pkg_list():
                    consoler.info(' \t\t pkg => %s' % h)

    logger.info('load end')

def telnet_ansible(server):
    """[测试托管服务器的ansible]
    
    Arguments:
        server {[list]} -- [对应服务器的ip]
    """

    if server[0] == 'all':
        ansible.telnet_module('all')
    else:
        for i in range(len(server)):
            if utils.valid_ip(server[i]):
                ansible.telnet_module(server[i])
            else:
                consoler.error('skip host %s, invalid host format.', server[i])


def start_server(chain_id):
    """[启动对应链的节点]
    
    Arguments:
        chain_id {[string]} -- [调用chain_id对应的链的所有服务器下的start.sh]
    """

    mm = meta.Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not start action, chain_id is %s', chain_id)
        return 

    logger.info('start action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.start_module(k, ansible.get_dir() + '/' + chain_id)


def stop_server(chain_id):
    """[停止对应链的节点]
    
    Arguments:
        chain_id {[string]} -- [调用chain_id对应的链的所有服务器下的stop.sh]
    """

    mm = meta.Meta(chain_id)

    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not stop action, chain_id is %s', chain_id)
        return 

    logger.info('stop action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.stop_module(k, ansible.get_dir() + '/' + chain_id)


def check_server(chain_id):
    """[检查对应链的节点]
    
    Arguments:
        chain_id {[string]} -- [调用chain_id对应的链的所有服务器下的check.sh]
    """

    mm = meta.Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not check action, chain_id is %s', chain_id)
        return 

    logger.info('check action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)


def monitor_server(chain_id):
    """[检查对应链的节点的运行情况, 调用monitor.sh脚本]
    
    Arguments:
        chain_id {[string]} -- [调用chain_id对应的链的所有服务器下的monitor.sh]
    """

    mm = meta.Meta(chain_id)
    if not mm.exist():
        logger.warn('chain meta is not exist, maybe the chain is not published, chain_id is %s', chain_id)
        consoler.warn('chain is not published, can not monitor action, chain_id is %s', chain_id)
        return 

    logger.info('monitor_server action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.monitor_module(k, ansible.get_dir() + '/' + chain_id)
