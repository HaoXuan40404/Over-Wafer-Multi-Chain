# coding:utf-8

from pys import path
from pys.log import consoler

def version():
    """load release_node.txt, print version number.
    """

    with open(path.get_path() + '/release_note.txt', 'r') as f:
        consoler.info(f.read())
