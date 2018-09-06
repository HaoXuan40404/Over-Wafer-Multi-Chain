class Ports:
    """
    object contains rpc p2p channel port
    """
    def __init__(self, rpc_port, p2p_port, channel_port):
        self.rpc_port = rpc_port
        self.p2p_port = p2p_port
        self.channel_port = channel_port
    
    def set_rpc_port(self, rpc_port):
        self.rpc_port = rpc_port

    def set_p2p_port(self, p2p_port):
        self.p2p_port = p2p_port
    
    def set_channel_port(self, channel_port):
        self.channel_port = channel_port
        
    def get_rpc_port(self):
        return self.rpc_port
    
    def get_p2p_port(self):
        return self.p2p_port
    
    def get_channel_port(self):
        return self.channel_port
    
    def __repr__(self):
        return 'Ports [rpc_port %u, p2p_port %u, channel_port %u]' % (self.rpc_port, self.p2p_port, self.channel_port)