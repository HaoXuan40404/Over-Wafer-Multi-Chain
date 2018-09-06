import utils

class Node:
    """
    object contains listenip and node count
    """
    def __init__(self, node_desc):
        self.node_desc = node_desc.strip()
        self.listen_ip = 0
        self.node_num = 0
    
    def doNodeParser(self):
        if isinstance(self.node_desc, str):
            l = self.node_desc.split()
            if len(l) != 2:
                raise Exception("node_desc invalid format", self.node_desc)
            if not utils.valid_ip(l[0]):
                raise Exception("invalid listen_ip format", l[0])
        else:
            raise Exception("node_desc node str type", self.node_desc)

    def getListenIp(self):
        return self.listen_ip
    
    def getNodeNum(self):
        return self.node_num
    
    def __repr__(self):
        return 'Node [listen_ip %s, node_num %u]' % (self.listen_ip, self.node_num)