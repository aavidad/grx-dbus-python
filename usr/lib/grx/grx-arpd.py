#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
from subprocess import Popen, PIPE, STDOUT
import gobject

arp='/usr/local/bin/arp-scan'

class Service(dbus.service.Object):

    def __init__(self, message):
        self._message = message

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName("grx.arp.service", dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/grx/arp/service")
        self._loop = gobject.MainLoop()
        print ("Servicio grx-arp arrancado...")
        self._loop.run()
        print ("Servicio grx-arp parado...")

    @dbus.service.method("grx.arp.service.equipos", in_signature='s', out_signature='s')
    def busca_equipo(self, g):
        cmd = [arp, '-q', '-x', g]
        proc = Popen(cmd, bufsize=4096, shell=False, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        string = proc.communicate()
        return string[0]

    @dbus.service.method("grx.arp.service.equipos", in_signature='ss', out_signature='s')
    def busca_equipos(self, origen, destino):
        cmd = ['/home/alberto/arp-scan', '-q', '-x', '-G', origen, destino]
        proc = Popen(cmd, bufsize=4096, shell=False, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        string = proc.communicate(input='2')
        return string[0]

    @dbus.service.method("grx.arp.service.equipos", in_signature='', out_signature='s')
    def busca_lista(self, lista):
        cmd = [arp, '-q', '-x', '-G', '50', '--file=-']
        proc = Popen(cmd, bufsize=4096, shell=False, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        string = proc.communicate(input=lista)
        return string[0]

    @dbus.service.method("grx.arp.service.Salir", in_signature='', out_signature='')
    def salir(self):
        print ("  Cerrando servicio grx.arp")
        self._loop.quit()

if __name__ == "__main__":
    Service("Servicio grx.arp").run()

