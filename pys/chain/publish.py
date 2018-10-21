# coding:utf-8
import os
from pys import utils
from pys import ansible
from pys.log import logger
from pys.log import consoler
from pys.chain import meta
from pys.chain import data
from pys.chain.chain import Chain
from pys.node import config

from pys.chain.chain import Chain


def publish_chain(chains):
    """publish operation.
    
    Arguments:
        list_chain_version {list} -- all chains need publish in the format of chain_id:chain_version, you can publish more than one at a time ,separate using spaces.
    """
    pchains = []
    for i in range(len(chains)):
        chain = chains[i].split(':')
        if len(chain) != 2:
            logger.error('not chain_id:chain_version format, str is %s', chains[i])
            consoler.error(' skip, invalid publish format, chain_id:chain_version should require, chain is %s', chain)
            continue

        chain_id = chain[0]
        chain_version = chain[1]

        pchains.append(Chain(chain_id, chain_version))
        # consoler.info('\t append publish chain, chain_id %s:chain_version %s', chain_id, chain_version)

        logger.debug('chain_id is %s, chain_version is %s', chain_id, chain_version)
            
    if len(pchains) != 0:
        for chain in pchains:
            logger.info('publish, chain_id is %s, chain_version is %s', chain_id, chain_version)
            publish_server(chain.get_id(), chain.get_version())


def publish_server(chain_id, chain_version):
    """publish one chain.

    Arguments:
        chain_id {string} -- chain id.
        chain_version {string} -- chain version.
    """

    chain = Chain(chain_id, chain_version)
    dir = chain.data_dir()
    if not os.path.isdir(dir):
        consoler.error(
            'publish install package for chain %s version %s failed, no package build for the chain.', chain_id, chain_version)
        logger.warn(
            'version of this chain is not exist, chain is %s, version is %s', chain_id, chain_version)
        return
    mm = meta.Meta(chain_id)
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            logger.debug('skip, not invalid host_ip ' + dir)
            continue
        ret = push_package(dir, host, chain_id, chain_version, meta)
        if ret:
            for list_dir in os.listdir(dir + '/' + host + '/'):
                if 'node' in list_dir:
                    cfg_json = dir + '/' + host + '/' + list_dir + '/config.json'
                    index = int(list_dir[4:])
                    cf = config.Config(chain_id)
                    if os.path.isfile(cfg_json):
                        cf.fromJson(cfg_json)
                        logger.debug(
                            ' load config success, index is %d, cf is %s', index, cf)
                    else:
                        logger.error(
                            ' load config failed, config is %s', cfg_json)
                        consoler.error(
                            ' load config failed, config is %s', cfg_json)
                    mm.append(meta.MetaNode(chain_version, host, cf.get_rpc_port(
                    ), cf.get_p2p_port(), cf.get_channel_port(), index))
    consoler.info(
        '\t\t publish install package for chain %s version %s end.', chain_id, chain_version)
    # record meta info, write meta.json file
    mm.write_to_file()

def push_package(dir, host, chain_id, version, meta, force = True):
    """push install package of one server
    
    Arguments:
        dir {string} -- package install dir       
        host {string} -- server host
        chain_id {string} -- chain id
        version {string} -- chain version
        force {string} -- is push all node dir or not published
    
    Returns:
        [bool] -- success return True, if not False will return.
    """
    # check if common dir exist.
    if not os.path.exists(dir + '/common'):
        logger.warn('common dir is not exist, dir is %s, host is %s', dir, host)
        return False

    # check if host dir exist.
    if not os.path.exists(dir + '/' + host):
        logger.warn('host dir is not exist, dir is %s, host is %s', dir, host)
        return False

    # create dir on the target server
    ret = ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('chain %s host %s, publish install package failed.', chain_id, host)
        return ret
    
    # push common package
    ret = ansible.copy_module(host, dir + '/common/', ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('chain %s host %s, push common dir failed.', chain_id, host)
        return ret
    
    if force:
        # push host dir
        ret = ansible.copy_module(host, dir + '/' + host + '/', ansible.get_dir() + '/' + chain_id)
        if not ret:
            consoler.error('chain %s host %s, publish install package failed', chain_id, host)
            return ret
    else:
        # push node${index} dir in host dir not published
        for list_dir in os.listdir(dir + '/' + host + '/'):
            if 'node' in list_dir:
                index = int(list_dir[4:])
                if meta.host_index_exist(host, index):
                    continue
                # push host dir
                ret = ansible.copy_module(host, dir + '/' + host + '/' + list_dir + '/', ansible.get_dir() + '/' + chain_id)
                if not ret:
                    consoler.error('chain %s host %s node is %s, publish node package failed', chain_id, host, list_dir)
                    return ret

    
    logger.info('push package success, dir is %s, host is %s, chain_id is %s, chain_version is %s', dir, host, chain_id, version)
    
    return True  




    

    





