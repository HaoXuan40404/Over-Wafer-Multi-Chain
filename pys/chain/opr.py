import os

from pys import ansible, utils
from pys.chain import meta
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
                    consoler.error('start_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('start_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.start_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.error('start_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('start_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])

            else:
                consoler.error('start_chain_resolve type error, chain[' + i + '] =>' + chain[i])
                logger.error('start_chain_resolve type error, chain[' + i + '] =>' + chain[i])


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
                    consoler.error('stop_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('stop_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.stop_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.error('stop_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('stop_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])

            else:
                consoler.error('stop_chain_resolve type error, chain[' + i + '] =>' + chain[i])
                logger.error('stop_chain_resolve type error, chain[' + i + '] =>' + chain[i])


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
                    consoler.error('check_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('check_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.check_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.error('check_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('check_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])

            else:
                consoler.error('check_chain_resolve type error, chain[' + i + '] =>' + chain[i])
                logger.error('check_chain_resolve type error, chain[' + i + '] =>' + chain[i])


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
                    consoler.error('monitor_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('monitor_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.monitor_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.error('monitor_chain_resolve error, %s is not a valid string',chain_get[0])
                    logger.error('monitor_chain_resolve, %s:%s is not a valid string',chain_get[0],chain_get[1])

            else:
                consoler.error('monitor_chain_resolve type error, chain[' + i + '] =>' + chain[i])
                logger.error('monitor_chain_resolve type error, chain[' + i + '] =>' + chain[i])


def list_chain_resolve(chain):
    if chain[0] == 'publish':
        chain = chain[1:]
        meta.list(chain)
    else:
        package.list(chain, False)


def echo_ansible(server):
    if server[0] == 'all':
        ansible.echo_module('all')
    else:
        for i in range(len(server)):
            if utils.valid_ip(server[i]):
                ansible.echo_module(server[i])
            else:
                consoler.error('skip host %s, invalid ip format.', server[i])


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
