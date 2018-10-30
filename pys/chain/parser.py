#coding:utf-8

import configparser
import logging
import codecs
import sys
import os

from pys import utils
from pys.log import logger, consoler

from pys.chain.chain import Chain
from pys.chain.port import Port
from pys.exp import MCError

class NodeEle:
    def __init__(self, node_desc):
        self.node_desc = node_desc.strip()
        self.host_ip = ''
        self.p2p_ip = ''
        self.node_num = 0
    
    def do_parser(self):

        l = self.node_desc.split()

        if len(l) < 3:
            raise Exception(" node_desc invalid format ", self.node_desc)

        if not utils.valid_ip(l[0]):
            raise Exception(" node_desc invalid format invalid host_ip ", l[0])
        if not utils.valid_ip(l[1]):
            raise Exception(" node_desc invalid format invalid p2p_ip ", l[1])
            
        if int(l[2]) <= 0:
            raise Exception(" node_desc invalid format node_num lt 0 ", l[2])
        self.host_ip = l[0]
        self.p2p_ip = l[1]
        self.node_num = int(l[2])

        logger.info(' cfg parser host ip is %s, p2p ip is %s, node_num is %d.', self.host_ip, self.p2p_ip, self.node_num)

    def get_host_ip(self):
        return self.host_ip

    def get_p2p_ip(self):
        return self.p2p_ip
    
    def get_node_num(self):
        return self.node_num
    
    def __repr__(self):
        return 'Node [host_ip %s, p2p_ip %s, node_num %d]' % (self.host_ip, self.p2p_ip, self.node_num)

class ConfigConf:
    """Configuration containing object[port], [node] and [chain]
    """
    def __init__(self, cfg):
        self.chain = None
        self.port = None
        self.cfg = cfg
        self.nodes = []
        self.parser()
    
    def __repr__(self):
        return 'ConfParser [ chain %s, ports %s, nodes %s ]' % (self.chain, self.port, self.nodes)

    def set_chain(self, chain):
        self.chain = chain

    def set_port(self, port):
        self.port = port
    
    def get_by_host_ip(self, host):
        for node in self.nodes:
            if node.get_host_ip() == host:
                return node
        return None

    def add_node(self, node):
        for n in self.nodes:
            if n.get_host_ip() == node.get_host_ip():
                return False
        self.nodes.append(node)
        return True

    def get_chain(self):
        return self.chain

    def get_port(self):
        return self.port
    
    def get_nodes(self):
        return self.nodes

    def get_cfg(self):
        return self.cfg

    def parser(self):
        '''
        resolve config.conf, return object[Config.conf]
        '''
        cfg = self.cfg
        logger.info('cfg parser %s', cfg)

        # read and parser config file
        cf = configparser.ConfigParser()
        with codecs.open(cfg, 'r', encoding='utf-8') as f:
            cf.readfp(f)

        chain_id = cf.get('chain', 'chainid')
        if not utils.valid_string(chain_id):
            raise Exception('chain_id empty.')
        
        if not utils.valid_chain_id(chain_id):
            raise Exception('invalid chain_id, ', chain_id)

        chain_version = cf.get('chain', 'version')
        if not utils.valid_string(chain_id):
            raise Exception('chain_version empty.')
        self.set_chain(Chain(chain_id, chain_version))

        rpc_port = cf.getint('ports', 'rpc_port')
        if not utils.valid_port(rpc_port):
            raise Exception('invalid rpc_port, ', rpc_port)
        p2p_port = cf.getint('ports', 'p2p_port')
        if not utils.valid_port(p2p_port):
            raise Exception('invalid p2p_port, ', p2p_port)
        channel_port = cf.getint('ports', 'channel_port')
        if not utils.valid_port(channel_port):
            raise Exception('invalid channel_port, ', channel_port)
        port = Port(rpc_port, p2p_port, channel_port)
        if port.check_port():
            raise Exception('port config dup, ', port)
        self.set_port(port)

        index = 0
        while True:
            try:
                n = NodeEle(cf.get('nodes', 'node%u' % index))
                index += 1
                n.do_parser()
            except Exception as e:
                logger.info('cfg parser end, e is %s, result is %s', e, self)
                break
            else:
                if not self.add_node(n):
                    raise Exception(' duplicate host ip, host is ', n.get_host_ip())
        
        if len(self.get_nodes()) == 0:
            raise Exception('invalid cfg format, nodes empty')

        logger.info('cfg parser end, result is %s', self)

class ConfigConfs:

    def __init__(self, cfg):
        self.cfg = cfg
        self.ccs = {}
        self.parser()
    
    def clear(self):
        self.ccs = {}

    def append(self, cc):
        chain = cc.get_chain()
        if not self.exist(chain):
            key = chain.get_id() + '_' + chain.get_version()
            self.ccs[key] = cc
            return True
        else:
            return False
    
    def get_ccs(self):
        return self.ccs
    
    def get_cc(self, chain):
        if self.exist(chain):
            return self.ccs[chain.get_id() + '_' + chain.get_version()]
        raise MCError(' cc not exist, chain %s' % chain)
    
    def exist(self, chain):
        key = chain.get_id() + '_' + chain.get_version()
        return key in self.ccs
    
    def get_cfg(self):
        return self.cfg

    def parser(self):

        self.clear()

        if os.path.exists(self.cfg) and os.path.isfile(self.cfg):

            logger.info(' single config is %s', self.cfg)
            # resolve one config.json
            try:
                self.append(ConfigConf(self.cfg))
            except Exception as e:
                logger.warn('parser cfg %s end exception, e is %s ', self.cfg, e)
                raise MCError(' parser config failed, invalid format, config is %s, exception is %s' % (self.cfg, e))

        elif os.path.isdir(self.cfg):
            logger.info(' config dir is %s', self.cfg)
            # resolve dir, if not config.json goto next
            for c in os.listdir(self.cfg):
                try:
                    logger.debug(' config dir is %s, config file is %s', self.cfg, c)
                    cc = ConfigConf(self.cfg + '/' + c)
                    chain = cc.get_chain()
                    if not self.append(cc):
                        cc = self.get_cc(chain)
                        logger.error(' chain_id：%s and chain_version：%s duplicate, config is %s:%s', chain.get_id(), chain.get_version(), cc.get_cfg(), c)
                        raise MCError(' chain_id：%s and chain_version：%s duplicate, config is %s:%s' % (chain.get_id(), chain.get_version(), cc.get_cfg(), c))
                    logger.debug(' append cc, cc is %s', cc)
                    consoler.info(' parser config %s success, chain_id is %s, chain_version is %s', c, chain.get_id(), chain.get_version())
                except Exception as e:
                    consoler.error(
                        ' skip config %s, invalid config format parser failed, exception is %s', c, e)
                    logger.warn(' parser cfg %s end exception, e %s ', c, e)

        else:
            raise MCError(' invalid config, neither directory nor file, config is %s' % self.cfg)