#coding:utf-8

import os
import sys
import shutil

from pys import path

class Data:
    data_dir = ''
    def __init__(self):
        pass
    
    def dir(self, chain_id, chain_version):
        return path.get_path() + ('./data/chain/pkg/' + chain_id + '/' + chain_version)

    def create(self, chain_id, chain_version):
        os.makedirs(dir(chain_id, chain_version))

    def exist(self, chain_id, chain_version):
        return os.path.isdir(self.dir(chain_id, chain_version))

    def remove(self, chain_id, chain_version):
        return shutil.rmtree(dir(chain_id, chain_version))