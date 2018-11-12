#coding:utf-8

import json
import subprocess
from pys.log import logger
"""Generate boots .json, which is a configuration file for nodes to perform p2p link

"""

class P2pHost:
    def __init__(self, host, p2pport):
        self.host = host
        self.p2pport = str(p2pport)

    def __repr__(self):
        return 'host %s, p2pport %s' % (self.host, self.p2pport)

class P2pHosts:
    def __init__(self):
        self.nodes = []

    def add_p2p_host(self, ph):
        self.nodes.append(ph)

    def __repr__(self):
        return 'nodes %s' % self.nodes

    def to_json(self):
        # return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)

    def clear(self):
        self.nodes = []
    
    def writeFile(self, file):
        try:
            with open(file, "w+") as f:
                f.write(self.to_json())
            logger.info(' write file success, file is %s', file)
        except Exception as e:
            logger.error(' write file failed, file is %s, exception is $s,', file, e)
            raise e

    def from_json(self, json):
        '''
        resolve bootstrapsnodes.json, convert to P2pHosts
        '''
        try:
            with open(json) as f:
                js = json.load(f)
                if 'nodes' in js:
                    for p in js['nodes']:
                        ph = P2pHost(p['host'], p['p2pport'])
                        print(' load host, host is %s ', ph)
                        self.add_p2p_host(ph)
                return True
        except Exception as e:
            print(' load bootstrapsnode.json failed, json is %s, e is %s ', json, e)
            return False
