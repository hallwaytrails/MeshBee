import os, logging

from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import TimeoutException, XBeeException

class Radio:
    def __init__(self, ip:str="10.0.0.1", port:str="/dev/ttyUSB0", baud:int=230400):
        self.ip = ip
        self.port = port
        self.baud = baud
        self.device = XBeeDevice(port, baud)
        self.device.open()
        self.max_payload_bytes = self.device.get_parameter("NP")
        self.xnet = self.device.get_network()

        # initial configuration
        self.device.set_parameter("NI", bytearray(ip, 'utf-8'))
        self.device.write_changes()

    def tx(self, destination_ip, payload):
        destination_node = self.xnet.get_device_by_node_id(destination_ip)
        if destination_node is None:
            # unpredictable behavior will result from duplicate NI's, the following picks the first
            destination_node = self.xnet.discover_device(destination_ip)
            if destination_node is None:
                return False
        
        try:
            self.device.send_data(destination_node, payload)
            return True
        except TimeoutException:
            pass
        except XBeeException:
            pass
        return False

    def poll(self):
        data = self.device.read_data()
        if data is not None:
            # XBeeMessage object
            return bytes(data.data)
        else:
            # None = no data w/in timeout (set to zero for instant)
            return None
