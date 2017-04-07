#!/usr/bin/env python

import dbus

class Cliente():
   def __init__(self):
      bus = dbus.SystemBus()
      service_arp = bus.get_object('grx.arp.service', "/grx/arp/service")
      service_sqlite = bus.get_object('grx.sqlite.service', "/grx/sqlite/service")

      self._busca_equipo = service_arp.get_dbus_method('busca_equipo', 'grx.arp.service.equipos')
      self._busca_equipos = service_arp.get_dbus_method('busca_equipos', 'grx.arp.service.equipos')
      self._busca_lista = service_arp.get_dbus_method('busca_lista', 'grx.arp.service.equipos')
      self._salir_arp = service_arp.get_dbus_method('salir', 'grx.arp.service.Salir')


      self._ip_nodos_mulhacen = service_sqlite.get_dbus_method('ip_nodos_mulhacen', 'grx.sqlite.service.nodos')
      self._crea_nodo = service_sqlite.get_dbus_method('crea_nodo', 'grx.sqlite.service.nodos')
      self._datos_nodo_por_nombre = service_sqlite.get_dbus_method('datos_nodo_por_nombre', 'grx.sqlite.service.nodos')
      self._datos_nodo_por_ip = service_sqlite.get_dbus_method('datos_nodo_por_ip', 'grx.sqlite.service.nodos')

      self._nombre_nodos = service_sqlite.get_dbus_method('nombre_nodos', 'grx.sqlite.service.nodos')
      self._salir_sqlite = service_sqlite.get_dbus_method('salir', 'grx.sqlite.service.Salir')



   def run(self):

      ip_nodos=self._ip_nodos_mulhacen()   #Extrae la ip de todos los nodos de la BD de sqlite.
      #print ip_nodos
      encontrados=self._busca_lista(ip_nodos) #Buscamos con arp los nodos y devolvemos los que responden
      #print encontrados
      #print "encontrados"
      nombre=self._nombre_nodos(encontrados)
      #print nombre
      nodo=self._datos_nodo_por_nombre(nombre)
      #print nodo
      nodo=self._datos_nodo_por_ip(encontrados)
      #print nodo

      crea=self._crea_nodo(nodo)
      #print crea
      #print self._datos_nodo_por_nombre("AGRON")
            
      
		      
if __name__ == "__main__":
   Cliente().run()

