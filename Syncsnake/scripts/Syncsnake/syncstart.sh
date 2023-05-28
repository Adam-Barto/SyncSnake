#!/bin/sh
onLogout() {
	pkill -f python
	exit
}
trap 'onLogout' SIGINT SIGHUP SIGQUIT SIGABRT SIGTERM
/usr/local/bin/python3 /Library/Scripts/Syncsnake/syncsnake.py
while true; do
	sleep 86400 &
	wait $!
done