############################################################################
# 
#  File: tundevice.py
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

import select
import logging
from pypacker.layer3 import ip
from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
from constants import LoggerNames

class TunDevice:
    def __init__(self, ip, netmask, mtu):
        self.logger = logging.getLogger(LoggerNames.TUN)
        self.tun = TunTapDevice(name='XBeeNet', flags=(IFF_TUN | IFF_NO_PI))
        self.tun.addr = ip
        self.tun.netmask = netmask
        self.tun.persist(True)
        self.tun.mtu=mtu
        self.tun.up()
        self.logger.info("Linux Tun device set up and ready to interface with mesh net")

        # setup polling
        self.poller = select.poll()
        self.poller.register(self.tun, select.POLLIN)

    def tx(self, payload):
        self.tun.write(payload)

    def poll(self, timeout):
        events = self.poller.poll(timeout)
        if events:
            data = self.tun.read(self.tun.mtu)
            pack = ip.IP(data)
            return {"IP": pack.dst, "payload": data}
        else:
            return None
