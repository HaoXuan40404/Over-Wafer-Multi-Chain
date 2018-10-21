#coding:utf-8

import os
import sys

class Path:
    '''
    Over-Wafer-Multi-Chain path configuration
    '''
    dir = ''
    fisco_path = '/usr/local/bin'

def set_fiso_path(fisco_dir):
    Path.fisco_path = fisco_dir

def get_fisco_path():
    return Path.fisco_path

def set_path(dir):
    Path.dir = dir

def get_path():
    return Path.dir
