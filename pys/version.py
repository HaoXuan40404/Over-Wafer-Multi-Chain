#coding:utf-8

import os

release_note_path=''

def set_release_note_path(p):
    global release_note_path
    release_note_path = p
    
def version():
    with open(release_note_path, 'r') as f:
        print(f.read())