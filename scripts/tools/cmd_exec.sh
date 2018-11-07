#!/bin/bash
EXIT_CODE=-1

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