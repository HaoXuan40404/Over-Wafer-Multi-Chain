#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
    cd $dirpath
    curdir=$PWD
    node=$(basename ${curdir})
    ./fisco-bcos --genesis ${curdir}/genesis.json  --config ${curdir}/config.json --export-genesis $1  > ${curdir}/fisco-bcos.log 2>&1

    echo "export genesis path => $1"