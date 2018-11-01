#coding:utf-8

import os
from pys.chain import data
import os

class Chain:
    """
    Chain object contains id and version of one chain and if it gm version.
    """

    def __init__(self, id, version, name = None):
        self.id = id
        self.version = version
        if name is None:
            self.name = str(id)
        else:
            self.name = name

    def __repr__(self):
        return '[Chain] id=%s, version=%s, name= %s' % (self.id, self.version, self.name)
    
    def set_id(self, id):
        self.id = id
    
    def set_version(self, version):
        self.version = version
    
    def set_name(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_version(self):
        return self.version
    
    def get_name(self):
        return self.name
    
    def exist(self):
        dir = self.data_dir()
        return os.path.exists(dir)
    
    def data_dir(self):
        return data.package_dir(self.get_id(), self.get_version())