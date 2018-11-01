#!/bin/bash

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

index=$1;

if [ -z $index ];then
    echo " diagnose all node of this server  ... "
    for diagnose in `ls $dirpath/node*/diagnose.sh`
    do
        bash $diagnose
    done
else
    #echo "start node$index ... "
    if [ -d node$index ];then
        bash node$index/diagnose.sh
    else
        echo "node$index diagnose.sh is not exist."
    fi
fi