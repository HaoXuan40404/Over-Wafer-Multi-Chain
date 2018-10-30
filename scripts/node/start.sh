#!/bin/bash

# bash start.sh      =>    start all node 
# bash start.sh IDX  =>    start the IDX node

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

index=$1;

if [ -z $index ];then
    echo "start all node ... "
    for startfile in `ls $dirpath/node*/start.sh`
    do
        bash $startfile
    done
else
    #echo "start node$index ... "
    if [ -d node$index ];then
        bash node$index/start.sh
    else
        echo "node$index is not exist."
    fi
fi
echo ""
