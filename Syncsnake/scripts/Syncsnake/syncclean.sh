#!/bin/sh
onLogout() {
	pkill -f python
	find ~/Desktop -delete
	exit
}
trap 'onLogout' SIGINT SIGHUP SIGQUIT SIGABRT SIGTERM
while true; do
	sleep 86400 &
	wait $!
done