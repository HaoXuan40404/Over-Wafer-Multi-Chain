# coding:utf-8

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
from pys.log import logger
from pys.log import consoler
from pys.chain import data
from pys.chain import package


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
