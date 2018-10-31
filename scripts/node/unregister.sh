#!/bin/bash
source /etc/profile
index=$1
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

if [ -d node$index ] && [ -f node$index/data/node.json ];then
    bash web3sdk/bin/web3sdk NodeAction cancelNode file:`pwd`/node$index/data/node.json
else
    echo "node$index/node.json is node exist."
fi