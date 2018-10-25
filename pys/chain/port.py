#coding:utf-8
import json
import os

from pys.log import logger
from pys.chain.package import HostNodeDirs
from pys.chain.package import VerHosts
from pys.chain.package import ChainVers
from pys.chain.package import AllChain
from pys.chain.chain import Chain
from pys.node import config
from pys.exp import MCError


class Port:
    """Port object contains rpc port、channel port、p2p port.
    """

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

    def to_port(self, index):
        return Port(self.get_rpc_port() + index, self.get_p2p_port() + index, self.get_channel_port() + index)

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def in_use(self, port):
        return port == self.rpc_port or port == self.p2p_port or port == self.channel_port

    def __repr__(self):
        return ' [rpc] %d, [p2p] %d, [channel] %d' % (self.rpc_port, self.p2p_port, self.channel_port)


class HostPort:
    def __init__(self, chain_id, chain_version, host):
        self.ports = {}
        self.chain_id = chain_id
        self.chain_version = chain_version
        self.host = host
        self.load()

    def __repr__(self):
        return ' chain id is %s, chain version is %s, host is %s, ports is %s' % (self.chain_id, self.chain_version, self.host, self.ports)

    def get_by_index(self, index):
        if self.ports.has_key(index):
            return self.ports[index]
        raise MCError(' not found, chain id is %s, chain version is %s, host is %s, index is %d' % (
            self.chain_id, self.chain_version, self.host, index))

    def get_chain_id(self):
        return self.chain_id

    def get_chain_version(self):
        return self.chain_version

    def get_host(self):
        return self.host
    
    def get_ports(self):
        return self.ports

    def clear(self):
        self.ports = {}

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def load(self):
        self.clear()

        hn = HostNodeDirs(self.chain_id, self.chain_version, self.host)
        host_dir = Chain(
            self.chain_id, self.chain_version).data_dir() + '/' + self.host + '/'
        for node in hn.get_node_dirs():
            cfg_json = host_dir + '/' + node + '/config.json'
            cf = config.Config(self.chain_id)
            if cf.fromJson(cfg_json):
                p = Port(int(cf.get_rpc_port()), int(
                    cf.get_p2p_port()), int(cf.get_channel_port()))
                self.ports[node] = p
                logger.debug(' append node, node is %s, port is %s', node, p)

        logger.info(' load end, hp ports is %s', self)


class ChainVerPort:

    def __init__(self, chain_id, chain_version):
        self.chain_version = chain_version
        self.chain_id = chain_id
        self.ports = {}
        self.load()

    def get_ports(self):
        return self.ports

    def __repr__(self):
        return ' chain id is %s, chain version is %s, ports is %s' % (self.chain_id, self.chain_version, self.ports)

    def get_chain_id(self):
        return self.chain_id

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def get_chain_version(self):
        return self.chain_version

    def get_by_host(self, host):
        if self.ports.has_key(host):
            return self.ports[host]
        raise MCError(' not found, chain id is %s, chain version is %s, host is %s' % (
            self.chain_id, self.chain_version, host))

    def clear(self):
        self.ports = {}

    def exist(self):
        dir = Chain(self.chain_id, self.chain_version).data_dir()
        return os.path.exists(dir)

    def load(self):

        self.clear()
        vh = VerHosts(self.chain_id, self.chain_version)
        for host in vh.get_pkg_list():
            hp = HostPort(self.chain_id, self.chain_version, host)
            self.ports[host] = hp

        logger.info('load end, cv ports len is %d', len(self.ports))


class ChainPort:

    def __init__(self, chain_id):
        self.chain_id = chain_id
        self.ports = {}
        self.load()

    def __repr__(self):
        return ' chain id is %s, ports is %s' % (self.chain_id, self.ports)

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def get_ports(self):
        return self.ports

    def clear(self):
        self.ports = {}

    def get_chain_id(self):
        return self.chain_id

    def get_by_chain_version(self, version):
        if self.ports.has_key(version):
            return self.ports[version]
        raise MCError(' not found, chain id is %s, chain version is %s' %
                      (self.chain_id, version))

    def load(self):

        cv = ChainVers(self.chain_id)
        for version in cv.get_ver_list():
            hp = ChainVerPort(self.chain_id, version)
            self.ports[version] = hp

        logger.info('load end, cp ports len is %d', len(self.ports))


class AllChainPort:
    def __init__(self):
        self.ports = {}
        self.load()

    def clear(self):
        self.ports = {}

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def get_ports(self):
        return self.ports

    def __repr__(self):
        return ' ports is %s' % (self.ports)

    def get_by_chain_id(self, chain_id):
        if self.ports.has_key(chain_id):
            return self.ports[chain_id]
        raise MCError(' not found, chain id is %s' % (chain_id))

    def get_all_ports_by_host(self, host):
        hps = []
        for cp in self.get_ports().itervalues():
            for cvp in cp.get_ports().itervalues():
                try:
                    hp = cvp.get_by_host(host)
                    logger.debug(' host is %s, hp is %s', host, hp)
                    hps.append(hp)
                except Exception as e:
                    pass
        logger.debug('host is %s, len is %d', host, len(hps))
        return hps

    def port_conflicts(self, chain_id, host, port):
        hps = self.get_all_ports_by_host(host)
        for hp in hps:
            if chain_id == hp.get_chain_id():
                continue
            for node in hp.get_ports().itervalues():
                if port.in_use(node.get_rpc_port()):
                    logger.info(
                        ' rpc port(%s) used by annother chain, host is %s, chain id is %s, chain version is %s, port is %s', str(node.get_rpc_port()), host, hp.get_chain_id(), hp.get_chain_version(), port)
                    raise MCError(' rpc port(%s) in use, host is %s, chain id is %s, chain version is %s, port is %s' % (
                        str(node.get_rpc_port()), host, hp.get_chain_id(), hp.get_chain_version(), port))

                if port.in_use(node.get_p2p_port()):
                    logger.info(
                        ' p2p port(%s) used by annother chain, host is %s, chain id is %s, chain version is %s, port is %s', str(node.get_p2p_port()), host, hp.get_chain_id(), hp.get_chain_version(), port)
                    raise MCError(' p2p port(%s) in use, host is %s, chain id is %s, chain version is %s, port is %s' % (
                        str(node.get_p2p_port()), host, hp.get_chain_id(), hp.get_chain_version(), port))
                if port.in_use(node.get_channel_port()):
                    logger.info(
                        ' channel port(%s) used by annother chain, host is %s, chain id is %s, chain version is %s, port is %s', str(node.get_channel_port()), host, hp.get_chain_id(), hp.get_chain_version(), port)
                    raise MCError(' channel port(%s) in use, host is %s, chain id is %s, chain version is %s, port is %s' % (
                        str(node.get_channel_port()), host, hp.get_chain_id(), hp.get_chain_version(), port))

    def load(self):

        ac = AllChain()
        for chain_id in ac.get_chains():
            cp = ChainPort(chain_id)
            self.ports[chain_id] = cp

        logger.info('load end, acp ports is %s', self.to_json())
