#!/bin/bash
#set -e
source ./scripts/tools/deps.sh

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

function alarm()
{
    local content=${1}
    echo -e "\033[31m ${content} \033[0m"
}

# check sudo permission
function sudo_permission_check() 
{
    sudo echo -n " "

    if [ $? -ne 0 ]; then
        alarm "no sudo permission, please add youself in the sudoers"; exit 1;
    fi
}

function format()
{
    dir=$1
    sudo find $dir -name "*.json"|  while read LINE; do  dos2unix $LINE  2>/dev/null ; done
    sudo find $dir -name "*.sh"|  while read LINE; do sudo chmod 777 $LINE; dos2unix $LINE 2>/dev/null ; done
    sudo find $dir -name "*.py"|  while read LINE; do sudo chmod 777 $LINE; dos2unix $LINE 2>/dev/null ; done
    sudo find $dir -name "web3sdk"|  while read LINE; do sudo chmod 777 $LINE; dos2unix $LINE 2>/dev/null ; done
}

#owmc install dir, default '/usr/local/'
install_dir="/usr/local/"
python_env='/usr/bin/python'
force="false"
gm="false"
owmc="/usr/bin/owmc"
function install()
{
    # sudo permission check
    sudo_permission_check

    py_version=$($python_env -V 2>&1 | awk {'print $2'} | awk -F. {' print $1"."$2"."$3 '})
    py_pip=pip -V 2>&1 | awk {'print $2'} | awk -F. {' print $1"."$2"."$3 '}

    # params check
    if [ -z "${py_version}" ];then
        alarm " not invalid python path, path is ${python_env}."; exit 1;
    fi

    echo " python version is ${py_version}, python path is ${python_env}"
    if [ os_check = "ubuntu" ];then
        sudo apt-get install python-pip
    elif [ os_check = "centos" ];then
        sudo yum install python-pip
    fi
    echo "install configparser "
    sudo pip install configparser

    if [ -f $owmc ];then
        if $force == "true";then
            sudo rm -rf $owmc
        else
            alarm " $owmc already install, set '-f' to force install." ; exit 1;
        fi
    fi

    if [ -d ${install_dir}/owmc/ ];then
        if $force == "true";then
            sudo rm -rf ${install_dir}/owmc
        else
            alarm " $owmc already install, set '-f' to force install." ; exit 1;
        fi
    fi

    echo " owmc install dir is ${install_dir}."
    echo " owmc python env is ${python_env}."

    sudo mkdir -p ${install_dir}/owmc
    sudo cp -r $dirpath/conf  ${install_dir}/owmc/
    sudo cp -r $dirpath/log  ${install_dir}/owmc/
    sudo cp -r $dirpath/pys  ${install_dir}/owmc/
    sudo cp -r $dirpath/scripts  ${install_dir}/owmc/
    sudo cp -r $dirpath/tpl  ${install_dir}/owmc/
    sudo cp -r $dirpath/doc  ${install_dir}/owmc/
    sudo cp -r $dirpath/data  ${install_dir}/owmc/
    sudo cp -r $dirpath/main.py  ${install_dir}/owmc/
    sudo cp -r $dirpath/release_note.txt ${install_dir}/owmc/
    format ${install_dir}/owmc/
    sudo sed -i "s|/usr/bin/python|${python_env}|g" ${install_dir}/owmc/main.py 1> /dev/null
    sudo sed -i "s|./log/all.log|${install_dir}/owmc/log/all.log|g" ${install_dir}/owmc/conf/logging.conf 1> /dev/null
    sudo ln -s ${install_dir}/owmc/main.py /usr/bin/owmc
    sudo chmod -R 777 ${install_dir}/owmc
    sudo chmod 777 /usr/bin/owmc

    # install deps and check if deps install success.
    bash $dirpath/scripts/tools/deps.sh "all"

    if [ $gm == "true" ];then
        echo " install gm deps tassl => "
        sudo chmod 777  ${install_dir}/owmc/scripts/ca/gm/install_tassl.sh
        sudo bash ${install_dir}/owmc/scripts/ca/gm/install_tassl.sh
    fi

    sudo chmod -R 777 $install_dir/owmc


    echo " owmc install success ! "
}

function help() 
{
    echo "Usage:"
    echo "Optional:"
    echo "    -d  <dir>           The dir of owmc will be install. (default: /usr/loca/)"
    echo "    -p  <path>          The python path. (default: /usr/bin/python) "
    echo "    -g                  Install guomi deps. (default: not install guomi deps.)"
    echo "    -f                  Install owmc even if it has been installed."
    echo "    -h                  This help."
    echo "Example:"
    echo "    bash install.sh "
    echo "    bash install.sh -d /usr/local -p /usr/bin/python -f -g "
    exit 0
}


while getopts "d:p:gfh" option;do
    case $option in
    d) install_dir=$OPTARG;;
    p) python_env=$OPTARG;;
    f) force="true";;
    g) gm="true";;
    h) help;;
    esac
done

# install
install
