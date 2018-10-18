#!/bin/bash

# bash start.sh      =>    start all node 
# bash start.sh IDX  =>    start the IDX node

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

index=$1;

if [ -z $index ];then
    total=999
    index=0
    echo "start all node ... "
    while [ $index -le $total ]
    do
        if [ -d node$index ];then
            bash node$index/start.sh
        else	
            break
        fi
        index=$(($index+1))
    done
else
    #echo "start node$index ... "
    if [ -d node$index ];then
        bash node$index/start.sh
    else
        echo "node$index is not exist."
    fi
fi
