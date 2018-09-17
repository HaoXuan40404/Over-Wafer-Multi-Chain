#coding:utf-8

import sys
import os

from pys import path
from pys import ca
from pys import version
# from pys.chain import build
from pys.chain import publish

def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径 
    pwd = os.getcwd()
    sys.path.append(pwd + '/pys')
    path.set_path(pwd)

    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')

def main():
    init()
    publish.publish_server('chain_1','v1')
    # build.chain_build(path.get_path() + '/conf/config.conf')
    #命令行 build publish start stop version_print

if __name__ == '__main__':

    main()
