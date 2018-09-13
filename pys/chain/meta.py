class ChainMeta:
    def __init__(self, chain_id):
        self.chain_id = chain_id
    
    def __repr__(self):
        return 'chain id is %s' % self.chain_id

    def get_chain_id(self):
        return self.chain_id