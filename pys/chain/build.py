from pys import log
from pys import utils
from pys import parser

import data

def build(cfg):
    p = parser.ConfParser(cfg)
    p.do_parser()
    cd = data.ChainData(p.get_chain_id(), p.get_chain_version())
    if cd.exist():
        raise Exception('chain_id on version exist, ', ('chainid is %s, version is %s') % (chain_id, chain_version) )
    
    


    