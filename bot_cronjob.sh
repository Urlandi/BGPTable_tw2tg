#!/bin/bash

set -o nounset

declare -r BASE_DIR='/opt/BGP-Table'
declare -r BOT_FILE='bgptable_tw2tg.py'
declare -r NOT_FOUND=1

ps ax | grep -q ${BOT_FILE}$

process_found=$?

if [ ${process_found} -eq ${NOT_FOUND} ]; then
    python3 ${BASE_DIR}/${BOT_FILE}&
fi
