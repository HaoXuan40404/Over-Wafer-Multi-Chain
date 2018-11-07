#!/bin/bash
###########################################################
# create by feinenxiang
###########################################################

EXIT_CODE=-1
cur_dir=`pwd`
GM_FOLDER=$(cd "$(dirname "$0")";pwd)
target_dir=${GM_FOLDER}

usage() {
printf "%s\n" "\
usage: command openssl_install_dir
notice: openssl_install_dir must be absolute path"
}

if [ -z "`echo $target_dir | grep '^/'`" -o -n "`echo $target_dir | grep '\.\.'`" ]; then
    usage
    exit $EXIT_CODE
fi

function LOG_ERROR() {
    local content=${1}
    echo -e "\033[31m"${content}"\033[0m"
}

function LOG_INFO() {
    local content=${1}
    echo -e "\033[32m"${content}"\033[0m"
}

function execute_cmd() {
    local command="${1}"
    eval ${command}
    local ret=$?
    if [ $ret -ne 0 ];then
        LOG_ERROR "${command} FAILED"
        exit $EXIT_CODE
    else
        LOG_INFO "${command} SUCCESS"
    fi
}

function need_install() {
    if [ ! -f "${target_dir}/bin/openssl" ];then
	    LOG_INFO "== TASSL has not been installed, install now! =="
    	return 1
    else
        LOG_INFO "== TASSL has been installed! =="
        return 0
    fi
}

function download_and_install() {
    need_install
    local required=$?
    if [ $required -eq 1 ];then
        local url=${1}
        local pkg_name=${2}
        local install_cmd=${3}
        
        local PKG_PATH=${cur_dir}/${pkg_name}
        git clone ${url}/${pkg_name}
        
        execute_cmd "cd ${pkg_name}"
        local shell_list=`find . -name *.sh`
        execute_cmd "chmod a+x ${shell_list}"
        execute_cmd "chmod a+x ./util/pod2mantest"
        execute_cmd "${install_cmd}"
        
        cd "${cur_dir}"
        execute_cmd "rm -rf ${PKG_PATH}"
    fi
}

function install_deps_centos() {
    execute_cmd "sudo yum -y install flex"
    execute_cmd "sudo yum -y install bison"
    execute_cmd "sudo yum -y install gcc"
    execute_cmd "sudo yum -y install gcc-c++"
}


function install_deps_ubuntu() {
    execute_cmd "sudo apt-get install -y flex"
    execute_cmd "sudo apt-get install -y bison"
    execute_cmd "sudo apt-get install -y gcc"
    execute_cmd "sudo apt-get install -y g++"
}

if grep -Eqi "Ubuntu" /etc/issue || grep -Eq "Ubuntu" /etc/*-release; then
    install_deps_ubuntu
else
    install_deps_centos
fi

tassl_name="TASSL"
tassl_url="https://github.com/jntass"
tassl_install_cmd="bash config --prefix=${target_dir} no-shared && make -j2 && make install"
download_and_install "${tassl_url}" "${tassl_name}" "${tassl_install_cmd}"

sed -i "s:{GM_PATH}:${GM_FOLDER}/bin/openssl:g" ${GM_FOLDER}/cert_tools.sh