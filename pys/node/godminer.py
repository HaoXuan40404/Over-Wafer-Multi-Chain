import json

class Miner:
    def __init__(self):
        self.Nodeid = ''
        self.Nodedesc = ''
        self.Agencyinfo = ''
        self.Peerip = ''
        self.Identitytype = 1
        self.Port = ''
        self.Idx = ''

    def set_nodeid(self, nodeid):
        self.Nodeid = nodeid

    def set_nodedesc(self, nodedesc):
        self.Nodedesc = nodedesc

    def set_agency(self, agency):
        self.Agencyinfo = agency
    
    def set_peerip(self, peerip):
        self.Peerip = peerip
    
    def set_port(self, port):
        self.Port = port

    def set_idx(self, idx):
        self.Idx = idx

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self, default = lambda obj : obj.__dict__, sort_keys=True, indent=4)
