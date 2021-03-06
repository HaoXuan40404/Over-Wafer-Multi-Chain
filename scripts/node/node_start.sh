#!/bin/bash

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
source ${dirpath}/../scripts/tools/port_check.sh
node=$(basename ${dirpath})
channelPort=`cat ${dirpath}/config.json | grep channelPort |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
rpcport=`cat ${dirpath}/config.json | grep rpcport |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
p2pport=`cat ${dirpath}/config.json | grep p2pport |grep -v grep|awk '{print $2}' | tr -cd "[0-9]"`
ulimit -c unlimited
weth_pid=`ps aux|grep "${dirpath}/config.json"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
if [ ! -z $weth_pid ];then
    echo " ${node} is running, pid is $weth_pid."
else 
    # port check
    check_port_use $channelPort 
    if [ $? -eq 0 ];then
        echo " ${node} channel port $channelPort already in use."
        exit 0
    fi
    check_port_use $rpcport
    if [ $? -eq 0 ];then
        echo " ${node} rpc port $rpcport already in use."
        exit 0
    fi
    check_port_use $p2pport
    if [ $? -eq 0 ];then
        echo " ${node} p2p port $p2pport already in use."
        exit 0
    fi
   
    echo " start ${node} ..."
    chmod a+x ../fisco-bcos
    nohup ../fisco-bcos  --genesis ${dirpath}/genesis.json  --config ${dirpath}/config.json  >> ${dirpath}/log/log 2>&1 &
fi

