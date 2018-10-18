# coding:utf-8

import os
import sys
import shutil
import json
import time

from pys import path
from pys.chain import data
from pys.log import logger
from pys.exp import MCError

class MetaNode:

    def __init__(self, version, host_ip, rpc_port, p2p_port, channel_port, index):
        self.host_ip = host_ip
        self.version = version
        self.rpc_port = rpc_port
        self.p2p_port = p2p_port
        self.channel_port = channel_port
        self.index = index

    def __repr__(self):
        return 'host %s, version %s, index %d, rpc %s, p2p %s, channel %s' % (self.host_ip, self.version, self.index, self.rpc_port, self.p2p_port, self.channel_port)


class Meta:

    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.nodes = {}

    def get_chain_id(self):
        return self.chain_id

    def get_host_nodes(self, host_ip):

        if self.nodes.has_key(host_ip):
            host_nodes = self.nodes[host_ip]
            logger.info(' get host nodes, host is %s, hm is %s',
                        host_ip, host_nodes)
        else:
            host_nodes = []
            logger.info(' get host nodes null, host is %s', host_ip)

        return host_nodes
    
    def host_index_exist(self, host_ip, index):
        if self.nodes.has_key(host_ip):
            host_nodes = self.nodes[host_ip]
            # assert len(host_nodes) != 0
            for node in host_nodes:
                if index == node.index:
                    logger.debug(' host index exist, host is %s, index is %d, host nodes is %s', host_ip, index, host_nodes)
                    return True
        logger.debug(' host index not exist, host is %s, index is %d, meta is %s', host_ip, index, self.to_json())
        return False

    def append(self, m):
        if self.host_index_exist(m.host_ip, m.index):
            return False
        if self.nodes.has_key(m.host_ip):
            host_nodes = self.nodes[m.host_ip]
            host_nodes.append(m)
        else:
            host_nodes = []
            host_nodes.append(m)
            self.nodes[m.host_ip] = host_nodes
        logger.info(' append mn failed, mn is %s, hm is %s', m, host_nodes)
        return True

    def get_nodes(self):
        return self.nodes

    def clear(self):
        self.nodes = {}

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def write_to_file(self):
        #if len(self.nodes) == 0:
        #    logger.debug('nodes empty, write return')
        #    return
        if not data.meta_dir_exist(self.chain_id):
            data.create_meta_dir(self.chain_id)

        meta_file = data.meta_dir(self.chain_id) + '/meta.json'
        meta_bak_file = meta_file + '_bak_' + \
            time.strftime("%Y-%m-%d_%H-%M%S", time.localtime())
        if os.path.exists(meta_file):
            shutil.copy(meta_file, meta_bak_file)
            logger.info(
                'meta.json is exist, backup it, name is ' + meta_bak_file)
        try:
            with open(data.meta_dir(self.chain_id) + '/meta.json', "w+") as f:
                f.write(self.to_json())
                logger.info(
                    'write info meta.json, content is ' + self.to_json())
        except Exception as e:
            logger.error(
                ' write meta failed, chaind id is %s, exception is %s', self.chain_id, e)
            # raise or not ???
            raise MCError(' write meta.json failed, chain id is %s, exception is %s' % (self.chain_id, e))

    def exist(self):
        return os.path.exists(data.meta_dir(self.chain_id) + '/meta.json')

    def load_from_file(self):
        self.clear()
        if not self.exist():
            logger.info(' meta.json not exist, chain_id is ' + self.chain_id)
            return

        try:
            with open(data.meta_dir(self.chain_id) + '/meta.json', 'r') as f:
                jsondata = json.load(f)
                if jsondata.has_key('nodes'):
                    for hm in jsondata['nodes'].values():
                        for v in hm:
                            mn = MetaNode(v['version'], v['host_ip'], v['rpc_port'],
                                          v['p2p_port'], v['channel_port'], v['index'])
                            logger.info(
                                'load from meta.json, meta node is %s', mn)
                            self.append(mn)
        except Exception as e:
            logger.error(
                ' load meta failed, chaind id is %s, exception is %s', self.chain_id, e)
            # raise or not ???
            raise MCError(' load meta.json data failed, chain id is %s, exception is %s' % (self.chain_id, e))
