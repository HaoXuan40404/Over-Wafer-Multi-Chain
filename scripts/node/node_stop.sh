#!/bin/bash
    dirpath="$(cd "$(dirname "$0")" && pwd)"
    cd $dirpath
    node=$(basename ${dirpath})
    weth_pid=`ps aux|grep "${dirpath}/config.json"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    kill_cmd="kill -9 ${weth_pid}"
    if [ ! -z $weth_pid ];then
        echo " stop ${node} ..."
        eval ${kill_cmd}
    else
        echo " ${node} is not running."
    fi