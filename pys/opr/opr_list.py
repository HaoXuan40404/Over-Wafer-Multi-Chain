# coding:utf-8
import os
import sys

from pys import ansible, utils
from pys.chain import data
from pys.chain.meta import *
from pys.chain.package import AllChain, ChainVers, HostNodeDirs, VerHosts
from pys.chain.port import HostPort
from pys.log import consoler, logger


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
        consoler.info(' => chain id ：%s    published version : %s', m.get_chain_id(), m.get_chain_version())
        nodes = m.get_nodes()
        for host, nodes in nodes.items():
            consoler.info('\t host => %s', host)
            for node in nodes:
                consoler.info('\t\t node => %s', node.get_node())

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
                    consoler.info('\t\t\t\t => %s %s ', node_dir, hp.get_by_index(node_dir))

    logger.info('load end')


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
            consoler.info(' \t => chain id ：%s    published version : %s', meta.get_chain_id(), meta.get_chain_version())
            nodes = meta.get_host_nodes(host)
            for node in nodes:
                consoler.info(' \t\t %s, rpc_port：%s, p2p_port：%s, channel_port：%s', node.get_node(), str(node.get_rpc()), str(node.get_p2p()), str(node.get_channel()))
