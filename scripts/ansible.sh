#!/bin/bash
#copy_module
function copy_module()
{
    local package_config=$1
    local ansible_src=$2
    local ansible_dest=$3
    ansible ${package_config} -m synchronize -a "src=${ansible_src} dest=${ansible_dest}"
}

###unarchive_module###
function unarchive_module()
{
    local package_config=$1
    local ansible_src=$2
    local ansible_dest=$3
    ansible ${package_config} -m unarchive -a "src=${ansible_src} dest=${ansible_dest}, mode=0755 copy=yes"

}

###start_module###
function start_module()
{
    local package_config=$1
    local start_path=$2
    ansible ${package_config} -m shell -a "bash ${start_path}/start.sh"
}

###stop_module###
function stop_module()
{
    local package_config=$1
    local stop_path=$2
    ansible ${package_config} -m shell -a "bash ${stop_path}/stop.sh"
}

###mkdir_module###
function mkdir_module()
{
    local package_config=$1
    local mkdir_path=$2
    ansible ${package_config} -m file -a "path=${mkdir_path} state=directory mode=0755"
}
###check_module###
function check_module()
{
    local package_config=$1
    local check_path=$2
    ansible ${package_config} -m shell -a "bash  ${check_path}/check.sh"
}
###monitor_module###
function monitor_module()
{
    local package_config=$1
    local check_path=$2
    ansible ${package_config} -m shell -a "bash  ${check_path}/monitor.sh"
}

###telnet_module###
function telnet_module()
{
    local package_config=$1
    local msg=$2
    ansible ${package_config} -m shell -a "echo $msg" 
}

###env_check### ansible远程调用检查目标服务器的操作系统版本;依赖项;
function env_check_module()
{
    local package_config=$1
    local check_path=$2
    ansible ${package_config} -m script -a "${check_path}/scripts/tools/os_check.sh && bash  ${check_path}/scripts/tools/deps_check.sh && bash  ${check_path}/scripts/tools/deps_install.sh"
}

###cmd_module###
function cmd_module()
{
    local package_config=$1
    local msg=$2
    ansible ${package_config} -m shell -a "$msg"
}

###file_module####
function file_module()
{
    local package_config=$1
    local ansible_src=$2
    local ansible_dest=$3
    ansible ${package_config} -m synchronize -a "src=${ansible_src} dest=${ansible_dest}"
}

case $1 in
    copy) copy_module $2 $3 $4;;
    unarchive) unarchive_module $2 $3 $4;;
    start) start_module $2 $3;;
    stop) stop_module $2 $3;;
    mkdir) mkdir_module $2 $3;;
    check) check_module $2 $3;;
    monitor) monitor_module $2 $3;;
    env_check) env_check_module $2 $3;;
    telnet) telnet_module $2 $3;;
    cmd) cmd_module $2 $3;;
    file) file_module $2 $3;;


    *) echo "others case";;
esac