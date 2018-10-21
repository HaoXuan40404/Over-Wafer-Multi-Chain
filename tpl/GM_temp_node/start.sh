#!/bin/bash
    dirpath="$(cd "$(dirname "$0")" && pwd)"
    cd $dirpath
    curdir=$PWD
    node=$(basename ${curdir})
    weth_pid=`ps aux|grep "${curdir}/config.json"|grep -v grep|awk '{print $2}'`
    if [ ! -z $weth_pid ];then
        echo "${node} is running, pid is $weth_pid."
    else
        echo "start ${node} ..."
        nohup ./fisco-bcos  --genesis ${curdir}/genesis.json  --config ${curdir}/config.json  --godminer godminer.json >> ${curdir}/log/log 2>&1 &
    fi
