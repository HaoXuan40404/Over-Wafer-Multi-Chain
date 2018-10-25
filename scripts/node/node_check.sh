#!/bin/bash
    dirpath="$(cd "$(dirname "$0")" && pwd)"
	cd $dirpath
    curdir=$PWD
    node=$(basename ${curdir})
    weth_pid=`ps aux|grep "$curdir/config.json"|egrep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    if [ ! -z $weth_pid ];then
        echo "${node} is running."
    else
        echo "${node} is not running."
    fi
