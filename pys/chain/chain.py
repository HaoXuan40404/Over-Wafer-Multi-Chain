#coding:utf-8

class Chain:
    '''
    描述一条区块链的chainid、版本号
    '''
    def __init__(self, id, version):
        self.id = id
        self.version = version

    def __repr__(self):
        return '[Chain] id=%s, version=%s' % (self.id, self.version)
    
    def set_id(self, id):
        self.id = id
    
    def set_version(self, version):
        self.version = version

    def get_id(self):
        return self.id

    def get_version(self):
        return self.version