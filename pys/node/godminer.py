import json

NODEID = '8c0fbe3a9b31775fc9786d7ae791e72b299d71bec18f18eb908caf637c71eaab4c691e738c41bc03478dd262077230056a4b0f07e9043445ea5632560326b8f5'
NODEDESC = 'temp'
AGENCYINFO = 'temp'
PEERIP = '127.0.0.1'
PORT = 30303
IDENTIFYTYPE = 1
IDX = 0

class Miner:
    def __init__(self):
        self.Nodeid = NODEID
        self.Nodedesc = NODEDESC
        self.Agencyinfo = AGENCYINFO
        self.Peerip = PEERIP
        self.Identitytype = IDENTIFYTYPE
        self.Port = PORT
        self.Idx = IDX

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

def build_godminer_json(ip, port):
    m = Miner()
    m.set_peerip(ip)
    m.set_port(port)
    return m.to_json()