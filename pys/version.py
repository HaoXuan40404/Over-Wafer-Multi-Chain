#coding:utf-8

from pys import path

def version():
    """打印当前版本号.
    """

    with open(path.get_path() + '/release_note.txt', 'r') as f:
        print(f.read())