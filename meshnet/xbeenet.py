############################################################################
# 
#  File: xbeenet.py
#  Copyright(c) 2023, Hallway Trails LLC. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

import threading
import logging
from radio import Radio
from tundevice import TunDevice
from constants import LoggerNames

class XBeeNet(threading.Thread):
    def __init__(self, configs):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(LoggerNames.NET)
        self.running = False
        self.configs = configs
        self.xbee = Radio(ip = self.configs['net']['ip'], 
                    port = self.configs['radio']['port'], 
                    baud = self.configs['radio']['baud'], 
                    net_id = self.configs['radio']['networkId'])
        self.tun = TunDevice(ip = self.configs['net']['ip'], 
                             netmask = configs['tun']['netmask'], 
                             mtu = self.xbee.get_mtu_int())

    def run(self):
        self.logger.info("Starting XBeeNet main running loop")
        self.running = True
        # main event loop
        while self.running:
            packet = self.tun.poll(10)
            if packet is not None:
                self.xbee.tx(packet['IP'], packet['payload'])
            packet = self.xbee.poll()
            if packet is not None:
                self.tun.tx(packet)
        self.logger.info("Exiting main XBeeNet running loop")

    def stop(self):
        self.running = False