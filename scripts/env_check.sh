#!/bin/bash
source $PWD/tools/os_check.sh
source $PWD/tools/deps_check.sh
source $PWD/tools/deps_install.sh
# check OS version
os_check
# check sudo permission
request_sudo_permission
# deps install
deps_install
# deps check
deps_check