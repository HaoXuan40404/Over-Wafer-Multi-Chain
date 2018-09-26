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