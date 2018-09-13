#coding:utf-8

import configparser
import logging
import codecs
import sys
import os

from basic import Chain
from pys import utils
from pys import log

class Port:
    '''
    端口
    '''
    def __init__(self, rpc_port, p2p_port, channel_port):
        self.rpc_port = rpc_port
        self.p2p_port = p2p_port
        self.channel_port = channel_port
    
    def set_rpc_port(self, rpc_port):
        self.rpc_port = rpc_port

    def set_p2p_port(self, p2p_port):
        self.p2p_port = p2p_port
    
    def set_channel_port(self, channel_port):
        self.channel_port = channel_port
        
    def get_rpc_port(self):
        return self.rpc_port
    
    def get_p2p_port(self):
        return self.p2p_port
    
    def get_channel_port(self):
        return self.channel_port
    
    def __repr__(self):
        return '[rpc_port] %d, [p2p_port] %d, [channel_port] %d' % (self.rpc_port, self.p2p_port, self.channel_port)

class NodeEle:
    def __init__(self, node_desc):
        self.node_desc = node_desc.strip()
        self.host_ip = ''
        self.p2p_ip = ''
        self.node_num = 0
    
    def do_parser(self):

        l = self.node_desc.split()

        if len(l) != 3:
            raise Exception("node_desc invalid format ", self.node_desc)

        if not utils.valid_ip(l[0]):
            raise Exception("node_desc invalid format invalid host_ip ", l[0])
        if not utils.valid_ip(l[1]):
            raise Exception("node_desc invalid format invalid p2p_ip ", l[1])
        if l[2] <= 0:
            raise Exception("node_desc invalid format node_num lt 0 ", l[2])
        self.host_ip = l[0]
        self.p2p_ip = l[1]
        self.node_num = int(l[2])

        log.get_logger().info('cfg parser host ip is %s, p2p ip is %s, node_num is %d', self.host_ip, self.p2p_ip, self.node_num)

    def get_host_ip(self):
        return self.host_ip

    def get_p2p_ip(self):
        return self.p2p_ip
    
    def get_node_num(self):
        return self.node_num
    
    def __repr__(self):
        return 'Node [host_ip %s, p2p_ip %s, node_num %d]' % (self.host_ip, self.p2p_ip, self.node_num)

class ConfParser:
    def __init__(self, cfg):
        self.config = cfg
        self.chain = None
        self.port = None
        self.nodes = []
    
    def __repr__(self):
        return 'ConfParser [ chain %s, ports %s]' % (self.chain, self.port)

    def do_parser(self):

        log.get_logger().info('cfg parser %s', self.config)

        if not utils.valid_string(self.config):
            raise Exception('config not string ', self.config)
        
        # read and parser config file
        cf = configparser.ConfigParser()
        with codecs.open(self.config, 'r', encoding='utf-8') as f:
            cf.readfp(f)
            
        chain_id = cf.get('chain', 'chainid')
        chain_version = cf.get('chain', 'version')
        self.chain = Chain(chain_id, chain_version)

        rpc_port = cf.getint('ports', 'rpc_port')
        p2p_port = cf.getint('ports', 'p2p_port')
        channel_port = cf.getint('ports', 'channel_port')
        self.port = Port(rpc_port, p2p_port, channel_port)

        index = 0
        while True:
            try:
                n = NodeEle(cf.get('nodes', 'node%u' % index))
                index += 1
                n.do_parser()
                self.nodes.append(n)
            except Exception, err:
                # log.get_logger().info('cfg parser end, result is %s', self)
                break
        
        if len(self.nodes) == 0:
            raise Exception('invalid cfg format, nodes empty')

        log.get_logger().info('cfg parser end, result is %s', self)

    def get_chain(self):
        return self.chain

    def get_port(self):
        return self.port
    
    def get_nodes(self):
        return self.nodes

def parser_test():
    log.init_logging('../../conf/logging.conf')
    confparser = ConfParser('../../conf/config.ini')
    confparser.do_parser()
    print(confparser.get_nodes())

if __name__ == '__main__':
    parser_test()