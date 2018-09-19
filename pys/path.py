#coding:utf-8

import os
import sys

class Path:
    '''
    multi-chain工作目录
    '''
    dir = ''
    fisco_dir = '/usr/local/bin'

def set_fiso_dir(fisco_dir):
    Path.fisco_dir = fisco_dir

def get_fisco_dir():
    return Path.fisco_dir

def set_path(dir):
    Path.dir = dir

def get_path():
    return Path.dir
