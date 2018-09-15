#!/bin/bash
    ulimit -c unlimited
    nohup ./build/fisco-bcos  --genesis ./build/node0/genesis.json  --config ./build/node0/config.json > ./build/node0/log/log 2>&1 &
