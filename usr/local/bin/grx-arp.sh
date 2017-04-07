#!/bin/bash
#/usr/local/bin/grx-arp.sh
#

function d_start()
{
	echo "grx-arp: Servicio iniciado" 
	/usr/lib/grx/grx-arpd.py --pidfile =/tmp/grx-arp.pid
	sleep  5 
	echo  "El PID es $(cat /tmp/grx-arp.pid)" 
}
 
function d_stop ( ) 
{ 
	echo "grx-arp: Parando el servicio (PID=$(cat /tmp/grx-arp.pid))" 
	kill $(cat  /tmp/grx-arp.pid ) 
	rm  /tmp/grx-arp.pid
 }
 
function d_status ( ) 
{ 
	ps  -ef | grep grx-arpd.py | grep -v grep 
	echo  "PID Estado $(cat /tmp/grx-arp.pid 2&gt;/dev/null) " 
}
 
# Esto siempre se ejecuta 
touch  /var/lock/grx-arp
 
# Management instructions of the service 
case  "$1"  in 
	start)
		d_start
		;; 
	stop)
		d_stop
		;; 
	reload)
		d_stop
		sleep  1
		d_start
		;; 
	status)
		d_status
		;; 
	* ) 
	echo  "Uso: $0 {start|stop|reload|status}" 
	exit  1 
	;; 
esac 
exit  0
