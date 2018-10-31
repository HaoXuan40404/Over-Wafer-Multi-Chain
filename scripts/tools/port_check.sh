#!/bin/bash
# Check if the port is occupied., need cmd -> nc -l
function check_port()
{
    type nc >/dev/null 2>&1
    if [ $? -ne 0 ];then
        echo "ERROR - nc is not installed."
        return
    fi

    nc -z 127.0.0.1 $1 >/dev/null 2>&1
    if [ $? -eq 0 ];then
        echo "$1 is listening."
    else
        echo "$1 is not listening."
    fi
}

function check_port_use()
{
    type nc >/dev/null 2>&1
    if [ $? -ne 0 ];then
        echo "ERROR - nc is not installed."
        return 0 
    fi

    nc -z 127.0.0.1 $1 >/dev/null 2>&1
    if [ $? -eq 0 ];then
        # echo "port $1 has been using."
        return 0
    else
        return 1
    fi
}
