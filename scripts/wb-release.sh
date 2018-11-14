#!/bin/bash

set -e

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
echo " dirpath is ${dirpath}"

host_ip=[@HOSTIP]
host_wan_ip=[@HOSTWANIP]
echo " host is ${host_ip}"
echo " host_wan_ip is ${host_wan_ip}"

function alarm()
{
    { echo 1>&2  "ERROR - $1"; exit 1; }
}

function dir_must_exist()
{
    local dir=$1
    if [ -d $dir ];then
        return
    fi

    alarm " $dir dir not exist. "
}

function file_must_exist()
{
    local file=$1
    if [ -f $file ];then
        return
    fi
    
    alarm " $file file not exist. "
}

function is_valid_ip()
{
    if [[ $1 =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        return 0
    else
        return 1
    fi
}

function ip_must_invalid()
{
    is_valid_ip $1
    if [ $? -ne 0 ];then
        alarm " invalid host ip, host is $host_ip. "
    fi
}

inner="false"
install_dir=$dirpath/../build
function install()
{
    local local_host=$host_wan_ip
    if [ $inner == "true" ];then
        local_host=$host_ip
    fi

    echo " install dir is ${install_dir} "
    echo " local host is ${local_host} "
    # check if common and host_ip dir exist
    dir_must_exist $dirpath/common
    dir_must_exist $dirpath/${local_host}
    ip_must_invalid $local_host
    file_must_exist $dirpath/common/scripts/tools/deps.sh

    # build dir
    mkdir -p ${install_dir}

    # copy common dir content to build dir.
    cp -rf $dirpath/common/* ${install_dir}/
    cp -rf $dirpath/$local_host/node* ${install_dir}/

    # install deps.
    bash $dirpath/common/scripts/tools/deps.sh "deps_install"
    bash $dirpath/common/scripts/tools/deps.sh "deps_check"

    # start all nodes.
    bash $install_dir/start.sh

    echo " install success !!! "
}

function help() 
{
    echo "Usage:"
    echo "Optional:"
    echo "    -i                  Inner ip or outer ip. "
    echo "    -d                  Install dir. Default : ../build. "
    echo "    -h                  This help."
    echo "Example:"
    echo "    bash production.sh -d /data/app/wetr-bcnode/build"
    exit 0
}


while getopts "d:ih" option;do
    case $option in
    i) inner="true";;
    d) install_dir=$OPTARG;;
    h) help;;
    esac
done

install
