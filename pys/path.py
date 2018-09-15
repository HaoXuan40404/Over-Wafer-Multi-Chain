#coding:utf-8

import os
import sys

class Path:
    '''
    multi-chain工作目录
    '''
    dir = ''

def set_path(dir):
    Path.dir = dir

def get_path():
    return Path.dir
