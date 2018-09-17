# coding:utf-8

import os
import sys
import shutil

from pys import path


class MetaNode:

   def __init__(self, version, host_ip, p2p_ip, p2p_port, channel_port, rpc_port):
        self.version = version
        self.host_ip = host_ip
        self.p2p_ip = p2p_ip
        self.p2p_port = p2p_port
        self.channel_port = channel_port
        self.rpc_port = rpc_port

    def __repr__(self):
        return self.to_json()
    
    def to_json(__self__):
        return json.dumps(self, default = lambda obj : obj.__dict__, indent=4)

class MetaNodes:
    def __init__(self):
        self.node_metas = []

    def append(self, m):
        self.node_metas.append(m)

    def to_json(self):
        return json.dumps(self, default = lambda obj : obj.__dict__, indent=4)

    def write_to_file(self, chain_id):
        with open(Meta().dir(chain_id), "w+") as f:
            f.write(to_json())

class Meta:
    data_dir = ''
    def __init__(self):
        pass
    
    def dir(self, chain_id):
        return path.get_path() + ('/data/chain/meta/' + chain_id)

    def create(self, chain_id):
        os.makedirs(dir(chain_id))
    
    def exist(self, chain_id):
        return os.path.isdir(self.dir(chain_id))

    def remove(self, chain_id):
        return shutil.rmtree(dir(chain_id))
