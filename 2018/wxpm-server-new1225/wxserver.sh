#!/bin/bash
function try_stop(){
    echo "Trying to stop services..."
    pgrep python | xargs kill
    echo "All services killed"
}
function try_start(){
    echo Trying to start all services...

    python WebServer.py >>/var/log/wxserver-$(date +%Y%m%d).log 2>&1 &
    python MatchingServer.py >>/var/log/matching-server-$(date +%Y%m%d).log 2>&1 &
}

function try_restart(){
    try_stop
    try_start
}


if [ -z "$1" ];then
    echo "usage: $0 start|stop|restart"
    exit
fi

action=$1

if [ "$action" = "stop" ]; then
    try_stop
elif [ "$action" = "start" ]; then
    try_start
elif [ "$action" = "restart" ]; then
    try_restart
fi