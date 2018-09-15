#coding:utf-8

import json

from pys.log import logger

'''
config.json的默认配置
'''
SEALENGINE = 'PBFT'
SYSTEMPROXYADDRESS = '0x0'
LISTEN_IP = '0.0.0.0'
CRYPTOMOD = '0'
RPCPORT = '8545'
P2PPORT = '30303'
CHANNELPORT = '8821'
WALLET = './keys.info'
KEYSTOREDIR = './keystore/'
DATADIR = './data/'
LOGVERBOSITY = '4'
COVERLOG = 'OFF'
EVENTLOG = 'ON'
STATLOG = 'ON'
LOGCONF = './log.conf'

class Config:
    '''
    fisco-bcos config.json配置文件对应的对象, 用来生成config.json文件
    '''
    def __init__(self, networkid):
        self.sealEngine = SEALENGINE
        self.systemproxyaddress = SYSTEMPROXYADDRESS
        self.listenip = LISTEN_IP
        self.cryptomod = CRYPTOMOD
        self.rpcport = RPCPORT
        self.p2pport = P2PPORT
        self.channelport = CHANNELPORT
        self.wallet = WALLET
        self.keystoredir = KEYSTOREDIR
        self.datadir = DATADIR
        self.networkid = networkid
        self.logverbosity = LOGVERBOSITY
        self.coverlog = COVERLOG
        self.eventlog = EVENTLOG
        self.statlog = STATLOG
        self.logconf = LOGCONF

    def set_sys_addr(self, addr):
        self.systemproxyaddress = addr
        
    def set_rpc_port(self, rpc_port):
        self.rpcport = rpc_port

    def set_p2p_port(self, p2p_port):
        self.p2pport = p2p_port

    def set_channel_port(self, channel_port):
        self.channelport = channel_port

    def __repr__(self):
        return self.toJson()

    def toJson(self):
        '''
        将config对象转换为json对象
        '''
        return json.dumps(self, default = lambda obj : obj.__dict__, indent=4)

    def fromJson(self, sjson):
        '''
        解析json字符串, 转换为config对象
        '''
        pass

def build_config_json(network_id, sys_addr = SYSTEMPROXYADDRESS, rpc_port = RPCPORT, p2p_port = P2PPORT, channel_port = CHANNELPORT):
    '''
    构造config.json
    '''
    cf = Config(network_id)
    cf.set_sys_addr(sys_addr)
    cf.set_rpc_port(rpc_port)
    cf.set_channel_port(channel_port)
    cf.set_p2p_port(p2p_port)
    logger.debug('config json is ' + cf.toJson())
    return cf.toJson()

    