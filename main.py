#coding:utf-8

import sys
import os
import logging

from pys import log
from pys import ca
from pys import version
from pys import data
from pys import build

def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径 
    pwd = os.getcwd()
    # logging初始化
    log.init_logging(pwd + '/conf/logging.conf')
    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')
    # 初始化数据目录
    data.set_data_dir(pwd + '/data/chain')
    # version
    version.set_release_note_path(pwd + '/release_note.txt')

def main():
    init()

if __name__ == '__main__':
    main()
