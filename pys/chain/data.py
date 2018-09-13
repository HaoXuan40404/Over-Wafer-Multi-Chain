#coding:utf-8

import os
import sys

class DataMgr:
    data_dir = ''
    def __init__(self):
        pass
    
    def dir(self, chain_id, chain_version):
        return DataMgr.data_dir + ('/pkg/%s/%s' % (chain_id, chain_version))

    def create(self, chain_id, chain_version):
        os.makedirs(dir(chain_id, chain_version))

    def exist(self, chain_id, chain_version):
        return os.path.isdir(dir(chain_id, chain_version))

    def remove(self, chain_id, chain_version):
        return os.removedirs(dir(chain_id, chain_version))

def set_data_dir(p):
    if not os.path.isdir(p):
        os.makedirs(p)
    DataMgr.data_dir = p

def get_data_dir():
    return DataMgr.data_dir

def data_test():
    set_data_dir(os.getcwd())
    cd = DataMgr()
    print(cd)
    print(cd.dir('123', '456'))

if __name__ == '__main__':
    data_test()