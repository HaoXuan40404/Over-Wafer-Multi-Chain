#coding:utf-8
import os
import sys

from pys import log
from pys import utils
from data import DataMgr

import parser

def build(cfg):

    log.get_logger().debug('building, cfg is %s', cfg)

    # 配置解析
    conf_parser = parser.ConfParser(cfg)
    conf_parser.do_parser()
    cdata = DataMgr()
    if cdata.exist(conf_parser.get_chain().get_id(), conf_parser.get_chain().get_version()):
        raise Exception('chainid with version already exist, id is %s, version is %s' % (conf_parser.get_chain().get_id(), conf_parser.get_chain().get_version()))
    
    # 构建安装包
    for node in conf_parser.get_nodes():
        print(node)

    


    