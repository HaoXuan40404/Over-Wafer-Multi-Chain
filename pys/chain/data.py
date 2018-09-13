#coding:utf-8

import os
import sys

class ChainData:
    data_dir = ''
    def __init__(self, chain_id, version):
        self.chain_id = chain_id
        self.version = version

    def __repr__(self):
        return 'chain is %s, version is %s' % (self.chain_id, self.version)
    
    def dir(self):
        return ChainData.data_dir + ('/pkg/%s/%s' % (self.chain_id, self.version))

    def create(self):
        os.makedirs(dir())

    def exist(self):
        return os.path.isdir(dir())

    def remove(self):
        return os.removedirs(dir())

def set_data_dir(p):
    if not os.path.isdir(p):
        os.makedirs(p)
    ChainData.data_dir = p

def get_data_dir():
    return ChainData.data_dir


def data_test():
    set_data_dir(os.getcwd())
    cd = ChainData('12345', 'v1.0')
    print(cd)
    print(cd.dir())

if __name__ == '__main__':
    data_test()