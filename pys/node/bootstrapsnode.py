#coding:utf-8

import json

class P2pHost:
    def __init__(self, host, p2pport):
        self.host = host
        self.p2pport = p2pport
    
    def __repr__(self):
        return 'host %s, p2pport %d' % (self.host, self.p2pport)

class P2pHosts:
    def __init__(self):
        self.nodes = []

    def add_p2p_host(self, ph):
        self.nodes.append(ph)

    def __repr__(self):
        return 'nodes %s' % self.nodes

    def to_json(self):
        return json.dumps(self, default = lambda obj : obj.__dict__, sort_keys=True, indent=4)

def bootstrapsnode_test():
    phs = P2pHosts()
    phs.add_p2p_host(P2pHost('127.0.0.1', 12345))
    phs.add_p2p_host(P2pHost('127.0.0.1', 12345))
    print(phs.to_json())
    print(phs)

if __name__ == '__main__':
    bootstrapsnode_test()