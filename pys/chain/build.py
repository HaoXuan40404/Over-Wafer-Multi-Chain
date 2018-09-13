from pys import log
from pys import utils
from data import ChainData

import parser

def build(cfg):

    log.get_logger().debug('building, cfg is %s', cfg)

    # 配置解析
    p = parser.ConfParser(cfg)
    p.do_parser()
    cdata = ChainData(p.get_chain_id(), p.get_chain_version())
    if cdata.exist():
        raise Exception('chainid with version already exist, id is %s, version is %s' % (p.get_chain_id(), p.get_chain_version())
    
    # 构建安装包
    for node in p.get_nodes():
        pass

    

    


    