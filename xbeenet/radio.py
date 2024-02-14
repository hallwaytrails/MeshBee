import sys
import subprocess
import logging
import serial
import time
from serial.serialutil import SerialException
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import TimeoutException, XBeeException
from constants import BAUDRATES

class Radio:
    def __init__(self, ip:str="10.0.0.1", port:str="/dev/ttyUSB0", baud:int=230400, net_id:int=0000):
        self.logger = logging.getLogger("Radio")
        self.ip = ip
        self.port = port
        self.baud = baud
        self.net_id = net_id
        self.device = XBeeDevice(port, baud)
        self.configure_from_scratch()

        try:
            self.device.open()
            self.logger.info(f'Serial connection to radio opened on {self.port}')
        except SerialException:
            self.logger.critical(f"Could not find the specified port: {self.port}")
            sys.exit(1)
        self.max_payload_bytes = self.device.get_parameter("NP")
        self.xnet = self.device.get_network()

        # initial configuration
        self.device.set_parameter("NI", bytearray(ip, 'utf-8'))
        self.device.set_parameter("ID", bytearray(self.net_id))
        self.device.write_changes()

    def baud_test(self):
        try:
            result = subprocess.check_output(['stty', '-F', self.port], stderr=subprocess.PIPE)
            rate = int(result.decode().split()[1])
        except subprocess.CalledProcessError:
            self.logger.critical("Unable to determine baud rate of device")
            sys.exit(1)
        return rate
    
    def serial_tx(self, serial_obj: serial.Serial, message):
        serial_obj.write(message)
        out = bytearray()
        time.sleep(2)
        while serial_obj.in_waiting > 0:
            out += serial_obj.read(1)
        return out.decode().strip()
    
    def validate_serial_response(self, response, expected):
        if response != expected:
            self.logger.critical(f'XBee failed to respond with expected output. Expected: {expected}, output: {response}')
            sys.exit(1)

    def configure_from_scratch(self):
        current_baud = self.baud_test()
        ser = serial.Serial(
            port = self.port,
            baudrate = current_baud
        )
        try:
            ser.open()
        except SerialException as e:
            if 'already open' in str(e):
                pass
            else:
                self.logger.critical('Unable to open a serial connection to device')
                sys.exit(1)
        # set in configure mode
        message = bytes('+++', 'utf-8')
        response = self.serial_tx(ser, message)
        self.validate_serial_response(response, 'OK')
        # Configure for API mode
        message = bytes('ATAP 2\r', 'utf-8')
        response = self.serial_tx(ser, message)
        self.validate_serial_response(response, 'OK')
        # Configure Desired Baud Rate
        message = bytes(f'ATBD {BAUDRATES[self.baud]}\r', 'utf-8')
        response = self.serial_tx(ser, message)
        self.validate_serial_response(response, 'OK')
        # Write the changes
        message = bytes(f'ATWR\r', 'utf-8')
        response = self.serial_tx(ser, message)
        self.validate_serial_response(response, 'OK')
        # Close configuration mode
        message = bytes(f'ATCN\r', 'utf-8')
        response = self.serial_tx(ser, message)
        self.validate_serial_response(response, 'OK')


        


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
