# coding:utf-8

from pys import path
from pys.log import consoler

def version():
    """读取release_node.txt, 打印版本号.
    """

    with open(path.get_path() + '/release_note.txt', 'r') as f:
        consoler.info(f.read())
