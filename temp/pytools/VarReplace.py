#!/usr/bin/python

import os
import sys
import commands
import json


class VarReplace(object):
		
    '''get json'''
    def get_new_json(self,filepath,key,value):
        key_ = key.split(".")
        #key_ = key
        key_length = len(key_)
        with open(filepath, 'rb') as f:
            json_data = json.load(f)
            i = 0
            a = json_data
            while i < key_length :
                if i+1 == key_length :
                    a[key_[i]] = value
                    i = i + 1
                else :
                    a = a[key_[i]]
                    i = i + 1
        f.close()
        return json_data

    '''write json'''	
    def rewrite_json_file(self,filepath,json_data):
        with open(filepath, 'w') as f:
            json.dump(json_data,f)
        f.close()

    '''just use them two
	   enter the path the key whick your want to changed and the value
	'''
    def get_to_write(self,filepath,key,value):

        m_json_data = self.get_new_json(filepath,key,value)	
        self.rewrite_json_file(filepath,m_json_data)

        return 0

    '''replace file str'''
    def replace_str(self, filepath, old_str, new_str):
        f = open(filepath,'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            line = line.replace(old_str, new_str)
            f.write(line)
        f.close()

    '''get file str'''
    def get_str(self, filepath):
        f = open(filepath,'r+')
        all_lines = f.readlines()
        #for line in all_lines:
        #    print(line)     
        f.close()
        return all_lines

    def get_json(self,filepath):
        file_json = filepath
        with open(file_json,'r+') as f:
            json_data = json.load(f)
            print(json_data,type(json_data))


if __name__=="__main__":
    '''main function'''
    print('main')
    test = VarReplace()
    filepath = '../tpl/node0/genesis.json'
    test.get_json(filepath)
