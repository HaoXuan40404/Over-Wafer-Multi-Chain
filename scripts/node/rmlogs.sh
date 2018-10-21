#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"

# clear log files, which last more than 3 hours。
for dir in `ls $dirpath | egrep "node[0-9]+"`
do
        if [ ! -d $dirpath/$dir/log ];then
                continue
        fi
        find  $dirpath/$dir/log -mtime +24 -type f -name "*log*log*" | xargs rm -rf
done
