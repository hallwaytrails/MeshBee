import select
import logging
from pypacker.layer3 import ip
from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI

class TunDevice:
    def __init__(self, ip, netmask, mtu):
        self.logger = logging.getLogger("TunDevice")
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
