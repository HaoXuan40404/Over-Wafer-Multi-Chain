# coding:utf-8

import os
import sys
import shutil
import json
import time

from pys import path
from pys.chain import data
from pys.log import logger, consoler

class MetaNode:

    def __init__(self, version, host_ip, rpc_port, p2p_port, channel_port):
        self.host_ip = host_ip
        self.version = version
        self.rpc_port = rpc_port
        self.p2p_port = p2p_port
        self.channel_port = channel_port

    def __repr__(self):
        return 'host %s, versionk %s' % (self.host_ip, self.version)
class Meta:
    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.nodes = {}
    
    def get_chain_id(self):
        return self.chain_id

    def append(self, m):
        self.nodes[m.host_ip] = m
    
    def get_nodes(self):
        return self.nodes

    def clear(self):
        self.nodes = {}
    
    def to_json(self):
        return json.dumps(self, default = lambda obj : obj.__dict__, indent=4)

    def write_to_file(self):
        if len(self.nodes) == 0:
            logger.debug('nodes empty, write return')
            return
        if not data.meta_dir_exist(self.chain_id):
            data.create_meta_dir(self.chain_id)
        meta_file = data.meta_dir(self.chain_id) + '/meta.json'
        meta_bak_file = meta_file + '_bak_' + time.strftime("%Y-%m-%d_%H-%M%S", time.localtime())
        if os.path.exists(meta_file):
            shutil.copy(meta_file, meta_bak_file)
            logger.info('meta.json is exist, backup it, name is ' + meta_bak_file)

        with open(data.meta_dir(self.chain_id) + '/meta.json', "w+") as f:
            f.write(self.to_json())
            logger.info('write info meta.json, content is ' + self.to_json())

    def load_from_file(self):
        self.clear()
        if not os.path.exists(data.meta_dir(self.chain_id) + '/meta.json'):
            logger.info('meta.json not exist, chain_id is ' + self.chain_id)
        with open(data.meta_dir(self.chain_id) + '/meta.json', 'r') as f:
            jsondata = json.load(f)
            if jsondata.has_key('nodes'):
                for v in jsondata['nodes'].values():
                    mn = MetaNode(v['version'], v['host_ip'], v['rpc_port'], v['p2p_port'], v['channel_port'])
                    logger.info('load from meta.json, meta node is %s', mn)
                    self.append(mn)

def list(chains):

    if len(chains) == 0:
        consoler.info('chains empty!')
    
    logger.info('list begin, chains is %s', chains)
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
        consoler.info('chain_id is %s' % m.get_chain_id())
        for index in range(len(m)):
            consoler.info('\t => %s' % m[index])

    logger.info('list end.')

def test_meta():
    m = Meta('12345')
    for i in range(10):
        m.append(MetaNode('version', '127.0.0.' + str(i), '8545', '30303', '8821'))
    
    m.write_to_file()
    m.load_from_file()

if __name__ == '__main__':
    test_meta()