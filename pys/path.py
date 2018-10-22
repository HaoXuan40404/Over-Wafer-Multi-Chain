#coding:utf-8

import os
import sys

class Path:
    '''
    Over-Wafer-Multi-Chain path configuration
    '''
    dir = ''

def set_path(dir):
    Path.dir = dir

def get_path():
    return Path.dir
