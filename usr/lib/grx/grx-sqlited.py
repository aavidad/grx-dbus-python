#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
import gobject
import os
import sqlite3
from random import randint

BASE_DATOS = "/var/lib/grx/conexiones.db"


class Service(dbus.service.Object):
    def __init__(self, message):
        self._message = message

# Funcion principal

    def run(self):
        global con
        con = sqlite3.connect(BASE_DATOS)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName("grx.sqlite.service", dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/grx/sqlite/service")

        self._loop = gobject.MainLoop()
        print ("Servicio grx-sqlite arrancado...")
        self._loop.run()
        print ("Cerrando base de datos...\n")
        con.close()
        print ("Servicio grx-sqlite parado...\n")

# ip_nodos_mulhacen
# Entrada:Ninguna
# Salida: Listado de todas las ip de la BD

    @dbus.service.method("grx.sqlite.service.nodos", in_signature='', out_signature='s')
    def ip_nodos_mulhacen(self):
        global con
        cursor = con.cursor()
        cursor.execute('''SELECT ip from NODOS''')
        tmp = '\n'.join(str(e[0]) for e in cursor)
        return tmp

    @dbus.service.method("grx.sqlite.service.nodos")
    def crea_nodo(self, lista):
        aleatorio = (randint(100, 239))
        todas_ip = ""
        if (lista != ""):
            nombre = lista[0][1]
            gw = lista[0][6]
            if (gw.split(".")[0] == "10"):
                DNS1 = "10.1.1.50"
                DNS2 = "10.1.1.4"
            else:
                DNS1 = "8.8.8.8"
                DNS2 = "8.8.6.6"
            for x in lista:
                red = x[6]
                ip = "ip4 " + red.split(".")[0] + "." + red.split(".")[1] + "." + red.split(".")[2] + "." + str(aleatorio) + " "
                todas_ip += ip
            if ((os.system('nmcli con add con-name ' + nombre + ' type ethernet ifname enp3s0 ' + todas_ip + ' gw4 ' + gw))!=0):
                print ("No ha sido posible crear " + nombre)
            if ((os.system('nmcli con mod ' + nombre + ' ipv4.dns "' + DNS1 + ',' + DNS2 + '"' + ' ipv4.dns-search "grx"'))!=0):
                print ("No ha sido posible anadir los DNS a la conexion " + nombre)
        return ("nada")

# nombre_nodos
# Entrada: Listado de ip's
# Salida: nombre de todos los nodos pasados en la lista

    @dbus.service.method("grx.sqlite.service.nodos", in_signature='s')
    def nombre_nodos(self, lista):
        global con
        tmp = ""
        cursor = con.cursor()
        for i in lista.splitlines():
            i = i.split('\t')[0]
            cursor.execute('''SELECT nombre from NODOS where ip=:ip''', {"ip": i})
            lst = '\n'.join(str(e[0]) for e in cursor)
            tmp = tmp + lst + "\n"
        return tmp

#   @dbus.service.method("grx.sqlite.service.nodos", in_signature='s')
#   def nombre_nodos(self,lista):
#      global con
#      tmp=[]
#      cursor = con.cursor()
#      for i in lista.splitlines():
#         i=i.split('\t')[0]
#         cursor.execute('''SELECT nombre from NODOS where ip=:ip''',{"ip": i})
#         for x in cursor:
#               tmp=tmp+[x]
#      return tmp

# datos_nodo_ip
# Entrada:
    @dbus.service.method("grx.sqlite.service.nodos", in_signature='s')
    def datos_nodo_por_ip(self, datos):
        global con
        tmp = []
        cursor = con.cursor()
        for i in datos.splitlines():
            i = i.split('\t')[0]
            cursor.execute('''SELECT * from NODOS where ip=:ip''',{"ip": i})
            for x in cursor:
                tmp = tmp + [x]
        return tmp

    @dbus.service.method("grx.sqlite.service.nodos", in_signature='s')
    def datos_nodo_por_nombre(self, datos):
        global con
        tmp = []
        cursor = con.cursor()
        for i in datos.splitlines():
            i = i.split('\t')[0]
            cursor.execute('''SELECT * from NODOS where nombre=:nombre''', {"nombre": i})
            for x in cursor:
                tmp = tmp + [x]
        return tmp

#   @dbus.service.method("grx.sqlite.service.nodos")
#   def datos_nodo_por_nombre(self,datos):
#      global con
#      tmp=()
#      cursor = con.cursor()
#      for i in datos:
#         print i
#         cursor.execute('''SELECT * from NODOS where nombre=:nombre''',{"nombre": i[0]})
#         for x in cursor:
#               tmp=tmp+(x)
#      return tmp

    @dbus.service.method("grx.sqlite.service.Salir", in_signature='', out_signature='')
    def salir(self):
        print ("  Cerrando servicio grx.sqlite")
        self._loop.quit()

if __name__ == "__main__":

    Service("Servicio grx.sqlite").run()
