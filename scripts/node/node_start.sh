#!/bin/bash

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
curdir=$PWD
source ${curdir}/../scripts/tools/port_check.sh
node=$(basename ${curdir})
channelPort=`cat ${curdir}/config.json | grep channelPort |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
rpcport=`cat ${curdir}/config.json | grep rpcport |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
p2pport=`cat ${curdir}/config.json | grep p2pport |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
ulimit -c unlimited
weth_pid=`ps aux|grep "${curdir}/config.json"|grep -v grep|awk '{print $2}'`
if [ ! -z $weth_pid ];then
    echo "${node} is running, pid is $weth_pid."
else 
    check_port_use $channelPort 
    channelPort_result=$?
    check_port_use $rpcport
    rpcport_result=$?
    check_port_use $p2pport
    p2pport_result=$?
    result=$channelPort_result || $rpcport_result || $p2pport_result
    if [ $result -eq 0 ];then
    echo "port is using, please check the port."
    else
        echo "start ${node} ..."
        chmod a+x ../fisco-bcos
        nohup ../fisco-bcos  --genesis ${curdir}/genesis.json  --config ${curdir}/config.json  >> ${curdir}/log/log 2>&1 &
    fi
fi

