#!/bin/bash
#/usr/local/bin/grx-sqlite.sh
#

function d_start()
{
	echo "grx-sqlite: Servicio iniciado" 
	/usr/lib/grx/grx-sqlited.py --pidfile =/tmp/grx-sqlite.pid
	sleep  5 
	echo  "El PID es $(cat /tmp/grx-sqlite.pid)" 
}
 
function d_stop ( ) 
{ 
	echo "grx-sqlite: Parando el servicio (PID=$(cat /tmp/grx-sqlite.pid))" 
	kill $(cat  /tmp/grx-sqlite.pid ) 
	rm  /tmp/grx-sqlite.pid
 }
 
function d_status ( ) 
{ 
	ps  -ef | grep grx-sqlited.py | grep -v grep 
	echo  "PID Estado $(cat /tmp/grx-sqlite.pid 2&gt;/dev/null) " 
}
 
# Esto siempre se ejecuta 
touch  /var/lock/grx-sqlite
 
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
