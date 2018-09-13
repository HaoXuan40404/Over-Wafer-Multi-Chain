#coding:utf-8

from pys import log
from pys import utils
from data import ChainData

from parser import ConfParser

def build(cfg):

    log.get_logger().debug('building, cfg is %s', cfg)

    # 配置解析
    p = ConfParser(cfg)
    p.do_parser()
    cdata = ChainData(p.get_chain_id(), p.get_chain_version())
    if cdata.exist():
        raise Exception('chainid with version already exist, id is %s, version is %s' % (p.get_chain_id(), p.get_chain_version())
    
    nodes = p.get_nodes()
    # 构建安装包
    for node in nodes:
        pass

    

    


    