import threading
import logging
from radio import Radio
from tundevice import TunDevice

class XBeeNet(threading.Thread):
    def __init__(self, configs):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger('XBeeNet')
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