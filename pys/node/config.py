#coding:utf-8

import json

from pys.log import logger

'''
config.json defaults
'''
SEALENGINE = 'PBFT'
SYSTEMPROXYADDRESS = '0xe4cd3e488cbf0a98e8ecd8bc5eefaf10e5d54905'
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
    Config object which use to generate config.json
    '''
    def __init__(self, networkid):
        self.sealEngine = SEALENGINE
        self.systemproxyaddress = SYSTEMPROXYADDRESS
        self.listenip = LISTEN_IP
        self.cryptomod = CRYPTOMOD
        self.rpcport = RPCPORT
        self.p2pport = P2PPORT
        self.channelPort = CHANNELPORT
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
        self.rpcport = str(rpc_port)

    def set_p2p_port(self, p2p_port):
        self.p2pport = str(p2p_port)

    def set_channel_port(self, channel_port):
        self.channelPort = str(channel_port)

    def get_rpc_port(self):
        return self.rpcport

    def get_p2p_port(self):
        return self.p2pport

    def get_channel_port(self):
        return self.channelPort

    def __repr__(self):
        return self.toJson()

    def toJson(self):
        '''
        convert config object to json object
        '''
        return json.dumps(self, default = lambda obj : obj.__dict__, indent=4)

    def fromJson(self, sjson):
        '''
        parser config file and generate config object.
        '''
        with open(sjson) as f:
            try : 
                js = json.load(f)
                self.systemproxyaddress = js['systemproxyaddress']
                self.rpcport = js['rpcport']
                self.p2pport = js['p2pport']
                self.channelPort = js['channelPort']
                logger.debug(' parser config success, cfg is %s, cfg_obj is %s', sjson, self)
                return True
            except Exception as e:
                logger.error(' parser config failed, cfg is %s, exception is %s', sjson, e)
                return False

def build_config_json(network_id, rpc_port = RPCPORT, p2p_port = P2PPORT, channel_port = CHANNELPORT):
    '''
    generate config.json
    '''
    cf = Config(network_id)
    cf.set_rpc_port(rpc_port)
    cf.set_channel_port(channel_port)
    cf.set_p2p_port(p2p_port)
    logger.debug('config json is ' + cf.toJson())
    return cf.toJson() 

def load_config_json(cfg):
    pass
