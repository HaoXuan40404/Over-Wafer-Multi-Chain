#coding:utf-8

import sys
import os
import logging

from pys import log
from pys import ca
from pys import version

def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径 
    pwd = os.getcwd()
    sys.path.append(os.getcwd() + '/pys')
    # logging初始化
    log.init_logging(pwd + '/conf/logging.conf')
    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')

def main():
    init()

if __name__ == '__main__':
    main()
