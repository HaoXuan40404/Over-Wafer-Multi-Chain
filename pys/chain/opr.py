import os

from pys import ansible, utils
from pys.chain import meta
from pys.chain.meta import Meta
from pys.chain.package import Package
from pys.log import logger
from pys.log import consoler
from pys.chain import data
from pys.chain import package


def start_chain_resolve(chain):
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        for chain_id in os.listdir(dir):
            start_server(chain_id)
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_string(chain_get[0]):
                    start_server(chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.start_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')

            else:
                consoler.info('chain_resolve error')
                logger.error('error chain_resolve')


def stop_chain_resolve(chain):
    if chain[0] == 'all':
        consoler.info('You want to stop all node,are you sure? yes or no? y/n')
        choice = raw_input('Your choice is: ')
        if ((choice == 'yes') | (choice == 'Yes') | (choice == 'Y') | (choice == 'y')):
            dir = data.meta_dir_base()
            for chain_id in os.listdir(dir):
                stop_server(chain_id)
        else:
            logger.info('refuse stop all node')
            return 0
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_string(chain_get[0]):
                    stop_server(chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.stop_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')

            else:
                consoler.info('chain_resolve error')
                logger.error('error chain_resolve')


def check_chain_resolve(chain):
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        for chain_id in os.listdir(dir):
            check_server(chain_id)
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_string(chain_get[0]):
                    check_server(chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.check_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')

            else:
                consoler.info('chain_resolve error')
                logger.error('error chain_resolve')


def monitor_chain_resolve(chain):
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        for chain_id in os.listdir(dir):
            monitor_server(chain_id)
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_string(chain_get[0]):
                    monitor_server(chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.monitor_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')

            else:
                consoler.info('chain_resolve error')
                logger.error('error chain_resolve')


def pub_list_resolve(chains):
    
    logger.info('list begin, chains is %s', chains)
    consoler.info(' chains is %s' % chains)

    meta_list = []
    if chains[0].trim() == 'all':
        dir = data.meta_dir_base()
        for chain_id in os.listdir(dir):
            m = Meta(chain_id)
            m.load_from_file()
            meta_list.append(m)
    else:
        for chain_id in chains:
            m = Meta(chain_id)
            m.load_from_file()
            meta_list.append(m)

    for m in meta_list:
        consoler.info(' => chain_id is %s' % m.get_chain_id())
        nodes = m.get_nodes()
        for node in nodes:
            consoler.info('\t node => %s' % node)

    logger.info('list end.')

def pkg_chain_resolve(chains, host_detail = True):

    logger.info('pkg_chain_resolve, chains is %s, host_detail is %s', chains, host_detail)

    consoler.info(' chains is %s' % chains)

    pkg_list = []
    if chains[0] == "all":
        dir = data.package_dir_base()
        for chain_id in os.listdir(dir):
            p = Package(chain_id)
            p.load()
            pkg_list.append(p)
    else:
        for chain_id in chains:
            p = Package(chain_id)
            p.load()
            pkg_list.append(p)

    for p in pkg_list:
        consoler.info(' => chain_id is %s' % p.get_chain_id())
        for v in p.get_version_list():
            consoler.info(' \t version : %s' % v.get_chain_version())
            if isinstance(host_detail, 'bool') and host_detail:
                for h in v.get_pkg_list():
                    consoler.info('\t\t package ' % h)

    logger.info('load end')

def echo_ansible(server):
    if server[0] == 'all':
        ansible.echo_module('all')
    else:
        for i in range(len(server)):
            if utils.valid_ip(server[i]):
                ansible.echo_module(server[i])
            else:
                consoler.info('\t [ERROR] skip host %s, invalid ip format.', server[i])


def start_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('start action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.start_module(k, ansible.get_dir() + '/' + chain_id)


def stop_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('stop action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.stop_module(k, ansible.get_dir() + '/' + chain_id)


def check_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k, v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.check_module(k, ansible.get_dir() + '/' + chain_id)


def monitor_server(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('monitor_server action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k in mm.get_nodes().iterkeys():
        logger.debug('host ip is ' + k)
        ansible.monitor_module(k, ansible.get_dir() + '/' + chain_id)
