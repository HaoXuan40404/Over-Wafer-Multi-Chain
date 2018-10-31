#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

# check if file exist, if not shell will exit with 1 returncode.
function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        echo " ${file} is not exist."
        exit 0
    fi
}

# echo with ip、time ahead
function alarm()
{
    alert_ip=`/sbin/ifconfig eth0 | grep inet | awk '{print $2}'`
    time=`date "+%Y-%m-%d %H:%M:%S"`
    echo "$alert_ip $1";
}

# check if blockchain consensus properly
function consensus_diagnose()
{
    # checkout if file exist.
    configfile=$dirpath/config.json
    check_file config.json
    config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
    config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")

    heightresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":67}')
    # echo $heightresult
    height=$(echo $heightresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [ -z "$height" ] &&  {
        echo " ERROR! Cannot connect to $config_ip:$config_port $heightresult"; 
        exit 0;
    }

    # heightvalue=$(printf "%d\n" "$height")
    viewresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_pbftView","params":[],"id":68}')
    # echo $viewresult
    view=$(echo $viewresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [ -z "$view" ] &&  {
        echo " ERROR! Cannot connect to $config_ip:$config_port $viewresult"; 
        exit 0;
    }

    # get PBFT view
    viewvalue=$(printf "%d\n" "$view")

    echo " height is $height and is view $view"
}

# diagnose why node not start success.
function running_diagnose()
{
    # checkout if file exist.
    configfile=$dirpath/config.json
    check_file ${configfile}

    node=$(basename ${dirpath})

    # check if fisco-bcos is running.
    fisco_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    if [ ! -z $fisco_pid ];then
        echo " ${node} is running."
        consensus_diagnose
        return 
    fi

    echo " ${node} is not running, start ${node}."

    # start node again
    bash $dirpath/start.sh
    sleep 10
    # check if fisco-bcos is running.
    fisco_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    if [ ! -z $fisco_pid ];then
        echo " start success, ${node} is running now."
        consensus_diagnose
        return
    fi 

    # find why node start failed?
    echo " start ${node} not success ."

    # check if core file exist.
    core_file_c=$(ls -lt core* | wc | awk '{print $1}')
    if [ ${core_file_c} -gt 1 ];then
        echo "  core file list ："
        ls -lt $dirpath/core* | awk '{print $9}' 
    fi

    # first log out log/log file content.
    if [ -s $dirpath/log/log ];then
        echo "  log/log content is "$(cat $dirpath/log/log)
    fi

    # find out last log file, and show out last 10 ERROR print.
    if [ ! -d $dirpath/log ];then
        echo "  log error message ："
        ls -lt log/log*.log | awk '{print $9}' | head -1 | xargs egrep "ERROR" | tail -10
    else
        echo " log dir not exist, dir is ${dirpath}/log"
    fi
}

running_diagnose