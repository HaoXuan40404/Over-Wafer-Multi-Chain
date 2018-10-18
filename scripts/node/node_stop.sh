#!/bin/bash
    dirpath="$(cd "$(dirname "$0")" && pwd)"
    cd $dirpath
    curdir=$PWD
    node=$(basename ${curdir})
    weth_pid=`ps aux|grep "${curdir}/config.json"|grep -v grep|awk '{print $2}'`
    kill_cmd="kill -9 ${weth_pid}"
    if [ ! -z $weth_pid ];then
        echo "stop ${node} ..."
        eval ${kill_cmd}
    else
        echo "${node} is not running."
    fi
