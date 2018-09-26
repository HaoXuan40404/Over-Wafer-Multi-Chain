#!/bin/bash

# 检查操作系统的版本, 目前支持的版本为: CentOS 7.2+ 64位, Ubuntu 16.04 64位
function os_check() 
{
    # Check for 'uname' and abort if it is not available.
    uname -v > /dev/null 2>&1 || { echo "ERROR - use 'uname' to identify the platform."; exit 1; }

    case $(uname -s) in 
    #------------------------------------------------------------------------------
    # Linux
    #------------------------------------------------------------------------------
    Linux)

        if [ ! -f "/etc/os-release" ];then
             { echo "ERROR - Unsupported or unidentified Linux distro."; exit 1; }
        fi

        DISTRO_NAME=$(. /etc/os-release; echo $NAME)
        echo "Linux distribution: $DISTRO_NAME."

        case $DISTRO_NAME in
    #------------------------------------------------------------------------------
    # Ubuntu 16.04
    #------------------------------------------------------------------------------
            Ubuntu*)

                echo "Running on Ubuntu."

                UBUNTU_VERSION=""
                type lsb_release >/dev/null 2>&1
                if [ $? -eq 0 ];then
                    UBUNTU_VERSION=$(lsb_release -r | awk '{print $2}')
                else
                    UBUNTU_VERSION=$(. /etc/os-release; echo $VERSION | awk '{print $1}')
                fi

                echo "Ubuntu Version => $UBUNTU_VERSION"

                ver=$(echo "$UBUNTU_VERSION" | awk -F . '{print $1$2}')
                # Ubuntu 16.04
                if [ $ver -ne 1604 ];then
                    { echo "ERROR - Unsupported Ubuntu Version. Ubuntu 16.04 is required."; exit 1; }
                fi

                ;;
    #------------------------------------------------------------------------------
    # CentOS  # At least 7.2
    #------------------------------------------------------------------------------
            CentOS*)
                echo "Running on CentOS."
                CENTOS_VERSION=""
                if [ -f /etc/centos-release ];then
                    CENTOS_VERSION=$(cat /etc/centos-release)
                elif [ -f /etc/redhat-release ];then
                    CENTOS_VERSION=$(cat /etc/redhat-release)
                elif [ -f /etc/system-release ];then
                    CENTOS_VERSION=$(cat /etc/system-release)
                fi

                if [ -z "$CENTOS_VERSION" ];then
                    { echo "ERROR - Unable to determine CentOS Version."; exit 1; }
                fi

                echo "CentOS Version => $CENTOS_VERSION"
                ver=$(echo "$CENTOS_VERSION" | awk '{print $4}' | awk -F . '{print $1$2}')

                #CentOS 7.2 or CentOS 7.2+
                if [ $ver -lt 72 ];then
                    { echo "ERROR - Unsupported CentOS Version. At least 7.2 is required. CentOS Version is ${CENTOS_VERSION}"; exit 1; }
                fi
                ;;
    #------------------------------------------------------------------------------
    # Oracle Linux Server # At least 7.4
    #------------------------------------------------------------------------------
            Oracle*) 
                echo "Running on Oracle Linux."
                ORACLE_LINUX_VERSION=""
                if [ -f /etc/oracle-release ];then
                    ORACLE_LINUX_VERSION=$(cat /etc/oracle-release)
                elif [ -f /etc/system-release ];then
                    ORACLE_LINUX_VERSION=$(cat /etc/system-release)
                fi

                if [ -z "$ORACLE_LINUX_VERSION" ];then
                    { echo "ERROR - Unable to determine Oracle Linux version."; exit 1; }
                fi

                echo "Oracle Linux Version => $ORACLE_LINUX_VERSION"
                ver=$(echo "$ORACLE_LINUX_VERSION" | awk '{print $5}' | awk -F . '{print $1$2}')

                #Oracle Linux 7.4 or Oracle Linux 7.4+
                if [ $ver -lt 74 ];then
                    { echo "ERROR - Unsupported Oracle Linux, At least 7.4 Oracle Linux is required."; exit 1; }
                fi

                ;;
    #------------------------------------------------------------------------------
    # Other Linux
    #------------------------------------------------------------------------------
            *)
                { echo "ERROR - Unsupported Linux distribution: $DISTRO_NAME."; exit 1; }
                ;;
        esac # case $DISTRO_NAME

        ;; #Linux)

    #------------------------------------------------------------------------------
    # Other platform (not Linux, FreeBSD or macOS).
    #------------------------------------------------------------------------------
    *)
        #other
        { echo "ERROR - Unsupported or unidentified OS."; exit 1; }
        ;;
    esac
}

# 安装依赖, yum/apt下载
function deps_install() 
{
    # Check for 'uname' and abort if it is not available.
    uname -v > /dev/null 2>&1 || { echo "ERROR - use 'uname' to identify the platform."; exit 1; }

    case $(uname -s) in 

    #------------------------------------------------------------------------------
    # Linux
    #------------------------------------------------------------------------------
    Linux)

        if [ ! -f "/etc/os-release" ];then
            { echo "ERROR - Unsupported or unidentified Linux distro."; exit 1; }
        fi

        DISTRO_NAME=$(. /etc/os-release; echo $NAME)
        # echo "Linux distribution: $DISTRO_NAME."

        case $DISTRO_NAME in
    #------------------------------------------------------------------------------
    # Ubuntu 16.04
    #------------------------------------------------------------------------------
            Ubuntu*)

                    sudo apt-get -y install lsof
                    sudo apt-get -y install gettext
                    sudo apt-get -y install bc
                    sudo apt-get -y install openssl
                    sudo apt-get -y install build-essential
                    sudo apt-get -y install libcurl4-openssl-dev libgmp-dev
                    sudo apt-get -y install libleveldb-dev  libmicrohttpd-dev
                    sudo apt-get -y install libminiupnpc-dev
                    sudo apt-get -y install libssl-dev libkrb5-dev
                    sudo apt-get -y install uuid-dev
                    sudo apt-get -y install vim-common

                ;;
    #------------------------------------------------------------------------------
    # CentOS  # At least 7.2
    #------------------------------------------------------------------------------
            CentOS*)

                    sudo yum -y install bc
                    sudo yum -y install gettext
                    sudo yum -y install openssl openssl-devel
                    sudo yum -y install leveldb-devel curl-devel 
                    sudo yum -y install libmicrohttpd-devel gmp-devel 
                    sudo yum -y install lsof
                    sudo yum -y install libuuid-devel
                    sudo yum -y install  vim-common

                ;;
    #------------------------------------------------------------------------------
    # Oracle Linux Server # At least 7.4
    #------------------------------------------------------------------------------
            Oracle*) 
                   
                    sudo yum -y install lsof
                    sudo yum -y install bc
                    sudo yum -y install gettext
                    sudo yum -y install openssl openssl-devel
                    sudo yum -y install leveldb-devel curl-devel 
                    sudo yum -y install libmicrohttpd-devel gmp-devel 
                    sudo yum -y install libuuid-devel

                ;;
    #------------------------------------------------------------------------------
    # Other Linux
    #------------------------------------------------------------------------------
            *)
                { echo "ERROR - Unsupported Linux distribution: $DISTRO_NAME."; exit 1; }
                ;;
        esac # case $DISTRO_NAME

        ;; #Linux)

    #------------------------------------------------------------------------------
    # Other platform (not Linux, FreeBSD or macOS).
    #------------------------------------------------------------------------------
    *)
        #other
        { echo "ERROR - Unsupported or unidentified OS."; exit 1; }
        ;;
    esac
}

# 权限检查
function request_sudo_permission() 
{
    sudo echo -n " "

    if [ $? -ne 0 ]; then
        { echo "ERROR - no sudo permission, please add youself in the sudoers."; exit 1; }
    fi
}

# 检查依赖软件是否安装, 使用type命令检查
function check_if_install()
{
    type $1 >/dev/null 2>&1
    if [ $? -ne 0 ];then
        { echo "ERROR - $1 is not installed."; exit 1; }
    fi
}

# java 版本检查
function java_version_check()
{
    check_if_install java

    check_if_install keytool

    #JAVA version
    JAVA_VER=$(java -version 2>&1 | sed -n ';s/.* version "\(.*\)\.\(.*\)\..*".*/\1\2/p;')
    echo $JAVA_VER
    if [ -z "$JAVA_VER" ];then
        { echo "ERROR - failed to get java version, version is `java -version 2>&1 | grep java`."; exit 1; }
    fi    

    #Oracle JDK 1.8
    if [ $JAVA_VER -eq 18 ] && [[ $(java -version 2>&1 ) ]];then
        #is java and keytool match ?
        JAVA_PATH=$(dirname `which java`)
        KEYTOOL_PATH=$(dirname `which keytool`)
        if [ "$JAVA_PATH" = "$KEYTOOL_PATH" ];then
            echo " java path => "${JAVA_PATH}
            echo " keytool path => "${KEYTOOL_PATH}
            return
        fi

        { echo "Oracle JDK 1.8 be requied, now JDK is `java -version 2>&1 | grep java`"; exit 1;}
    fi
    
    { echo "Oracle JDK 1.8 be requied, now JDK is `java -version 2>&1 | grep java`"; exit 1; }
} 

# openssl版本检查
function openssl_version_check()
{
    check_if_install openssl

    #openssl version
    OPENSSL_VER=$(openssl version 2>&1 | sed -n ';s/.*OpenSSL \(.*\)\.\(.*\)\.\([0-9]*\).*/\1\2\3/p;')

    if [ -z "$OPENSSL_VER" ];then
        { echo  "failed to get openssl version, version is `openssl version`" ; exit 1; }
    fi

    #openssl 1.0.2
    if [ $OPENSSL_VER -eq 102 ];then
        return 
    fi

    { echo "OpenSSL 1.0.2 be requied , now OpenSSL version is `openssl version`" ; exit 1; }
}

# version check
function deps_check()
{
    # java => Oracle JDK 1.8
    java_version_check
    # openssl => OpenSSL 1.0.2
    openssl_version_check

    # lsof
    check_if_install lsof
    # envsubst
    check_if_install envsubst
    # xxd
    check_if_install xxd
    # bc
    check_if_install bc

    # add more check here
}



# check OS version
os_check
# check sudo permission
request_sudo_permission
# deps install
deps_install
# deps check
deps_check