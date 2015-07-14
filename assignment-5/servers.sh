#!/bin/bash
ip=$1

# declare -A ip

# ip[e1]=10.0.0.1
# ip[e2]=10.0.0.2
# ip[e3]=10.0.0.3
# ip[w1]=10.0.0.4
# ip[w2]=10.0.0.5
# ip[w3]=10.0.0.6

function start_servers(){
	ip=$1
	ports=(1234 1080 2000 2001 2002 2003 2004 3000 3001 3002 8000 9000)

	for port in ${ports[*]}
	do
		printf '%s %s\n' $host_name $port
		python test-server.py $ip $port 2>&1 | tee -a output.txt &
	done	
}


cmd=$1
echo "Running: " $cmd


case "$cmd" in 
	start )
		ip=$2
		start_servers $ip
		;;
	list )
		ps -Ao pid,cmd | grep test-server.py
	;; 
	kill )
		pkill -f "test-server.py $2"
	;;

esac
