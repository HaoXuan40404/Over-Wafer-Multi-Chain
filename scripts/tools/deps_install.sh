#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
source $dirpath/deps.sh

deps_install
deps_check