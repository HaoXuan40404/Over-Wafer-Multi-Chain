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
        return path.get_path() + ('/data/chain/pkg/' + chain_id + '/' + chain_version)
    
    def exist(self, chain_id, chain_version):
        return os.path.isdir(self.dir(chain_id, chain_version))

    def remove(self, chain_id, chain_version):
        return shutil.rmtree(dir(chain_id, chain_version))

def package_dir(chain_id, chain_version):
    return path.get_path() + ('/data/chain/pkg/' + chain_id + '/' + chain_version)

def meta_dir_base():
    return path.get_path() + ('/data/chain/meta/')
    
def meta_dir(chain_id):
    return path.get_path() + ('/data/chain/meta/' + chain_id)

def package_dir_exist(chain_id, chain_version):
    return os.path.isdir(package_dir(chain_id, chain_version)) 

def create_package_dir(chain_id, chain_version):
    os.makedirs(package_dir(chain_id, chain_version))

def remove_package_dir(chain_id, chain_version):
    return shutil.rmtree(package_dir(chain_id, chain_version))

def meta_dir_exist(chain_id):
    return os.path.isdir(meta_dir(chain_id)) 

def create_meta_dir(chain_id):
    os.makedirs(meta_dir(chain_id))

def remove_meta_dir(chain_id):
    shutil.rmtree(meta_dir(chain_id))