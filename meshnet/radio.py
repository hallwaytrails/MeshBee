import sys
import subprocess
import logging
import serial
import time
from serial.serialutil import SerialException
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import TimeoutException, XBeeException
from constants import BAUDRATES, DEFAULT_MTU

class Radio:
    def __init__(self, ip:str="10.0.0.1", port:str="/dev/ttyUSB0", baud:int=230400, net_id:int=1111):
        self.logger = logging.getLogger("Radio")
        self.ip = ip
        self.port = port
        self.baud = baud
        self.net_id = net_id
        self.device = XBeeDevice(port, baud)
        self.max_payload_bytes = None
        self.perform_initial_configuration()
        self.set_mtu_int(self.device.get_parameter("NP"))
        self.xnet = self.device.get_network()      

    # Perform all initial configuration for an XBee device, agnostic to previous settings     
    def perform_initial_configuration(self):
        # First lets check that a device is even connected
        self.device_check()
        # Determine the current baud rate
        # This will also determine if a device is connected
        current_baud = self.baud_and_device_test()
        self.configure_for_api_mode(current_baud)

        if not self.device.is_open():
            try:
                self.device.open()
                self.logger.info(f'Serial connection to radio opened on {self.port}')
            except SerialException:
                self.logger.critical(f"Could not find the specified port: {self.port}")
                sys.exit(1)
        else:
            self.logger.info(f"Serial connection to radio already open on {self.port}")

        # initial configuration
        self.device.set_parameter("NI", bytearray(self.ip, 'utf-8'))
        # The Net ID takes a little processing
        self.device.set_parameter('ID', self.convert_netid())
        self.device.write_changes()
        self.logger.info("XBee fully configured and ready to interface with mesh net")

    # Process the net ID from the config input integer to the bytearray required for xbee input
    def convert_netid(self):
        # The Net ID takes a little processing
        if type(self.net_id) is not int:
            try:
                self.net_id = int(self.net_id)
            except ValueError:
                self.logger.warning("Detected non-integer type input for Network ID. Must be an integer between 0-32767. Using default Network Id of 1111")
                self.net_id = 1111
        elif self.net_id < 0 or self.net_id > 32767:
            self.logger.warning("Network ID input is out of range. Must be an integer between 0-32767. Using default Network Id of 1111")
            self.net_id = 1111
        return bytearray.fromhex(hex(self.net_id)[2:])

    # Check that the expected device actually exists
    def device_check(self):
        try:
            result = subprocess.check_output(['ls', f'{self.port}'])
            result_decoded = result.decode()
            if 'No such file or directory' in result_decoded: raise FileNotFoundError
            self.logger.info(f"Radio device detected over serial at {self.port}")
        except FileNotFoundError:
            self.logger.critical(f'Unable to find specified device: {self.port}')
            sys.exit(1)

    # Determine if the Xbee is in API mode or not
    def in_api_mode(self, baud_rate) -> bool:
        # open a serial connection
        ser_conn = self.open_raw_serial(baud_rate)
        # send message to go into command mode. If Ok response, then 
        # xbee is not in transparent mode
        message = bytes('+++', 'utf-8')
        response = self.serial_tx(ser_conn, message)
        self.validate_serial_response(response, 'OK')
        # Send a message requesting API mode status
        message = bytes('ATAP\r', 'utf-8')
        response = self.serial_tx(ser_conn, message)
        if response in ['1', '2']:
            return True
        return False

    # Test if device is connected and find its baud rate
    def baud_and_device_test(self):
        for rate in BAUDRATES:
            ser_conn = self.open_raw_serial(rate)
            message = bytes('+++', 'utf-8')
            response = self.serial_tx(ser_conn, message)
            if response == 'OK':
                self.logger.info(f'Current baud rate to device determined to be {rate}')
                return rate
        # If we cannot determine the baud rate or communicate with an XBee,
        # we cannot continue so exit here
        self.logger.critical("Unable to determine baud rate of device")
        sys.exit(1)
    
    # Send a message over a raw serial connection
    def serial_tx(self, serial_obj: serial.Serial, message):
        serial_obj.write(message)
        out = bytearray()
        time.sleep(2)
        while serial_obj.in_waiting > 0:
            out += serial_obj.read(1)
        return out.decode().strip()
    
    # Open a raw serial connection
    def open_raw_serial(self, baud) -> serial.Serial:
        try:
            serial_connection = serial.Serial(
                port = self.port,
                baudrate = baud
            )
            if not serial_connection.is_open:
                serial_connection.open()
        except SerialException:
                return None
        return serial_connection
    
    # Validate a response from serial against an expected response
    # Die if expected response is not given
    def validate_serial_response(self, response, expected):
        if response != expected:
            self.logger.critical(f'XBee failed to respond with expected output. Expected: {expected}, output: {response}')
            sys.exit(1)

    # Perform configuration for an XBee not in API mode
    def configure_for_api_mode(self, baud_rate):
        serial = self.open_raw_serial(baud_rate)
        # set in configure mode
        message = bytes('+++', 'utf-8')
        response = self.serial_tx(serial, message)
        self.validate_serial_response(response, 'OK')
        # Configure for API mode
        message = bytes('ATAP 2\r', 'utf-8')
        response = self.serial_tx(serial, message)
        self.validate_serial_response(response, 'OK')
        # Configure Desired Baud Rate
        message = bytes(f'ATBD {BAUDRATES[self.baud]}\r', 'utf-8')
        response = self.serial_tx(serial, message)
        self.validate_serial_response(response, 'OK')
        # Write the changes
        message = bytes(f'ATWR\r', 'utf-8')
        response = self.serial_tx(serial, message)
        self.validate_serial_response(response, 'OK')
        # Close configuration mode
        message = bytes(f'ATCN\r', 'utf-8')
        response = self.serial_tx(serial, message)
        self.validate_serial_response(response, 'OK')
        # Wait a second for the Xbee to settle from closing command mode
        time.sleep(1)
        if not self.in_api_mode(self.baud):
            self.logger.critical("Attempted and failed to configure XBee for API mode")
        else:
            self.logger.info("XBee properly configured for API mode")

    # Set the MTU
    def set_mtu_int(self, mtu_bytes):
        try:
            self.max_payload_bytes = int.from_bytes(mtu_bytes, byteorder='big', signed=False)
        except:
            self.logger.warning(f"Unable to set MTU into int, likely invalid input for MTU bytes. Using default of {DEFAULT_MTU}. Input: {mtu_bytes}")
            self.max_payload_bytes = DEFAULT_MTU

    # Get the MTU
    def get_mtu_int(self):
        return self.max_payload_bytes

    def tx(self, dest_ip_bytes, payload):
        dest_ip_hex = dest_ip_bytes.hex()
        dest_ip_NI = (str(int(dest_ip_hex[:2], 16)) + '.' + 
                      str(int(dest_ip_hex[2:4], 16)) + '.' + 
                      str(int(dest_ip_hex[4:6], 16)) + '.' + 
                      str(int(dest_ip_hex[6:8], 16)))
        self.logger.info(f"Sending to NI: {dest_ip_NI}")
        destination_node = self.xnet.get_device_by_node_id(dest_ip_NI)
        if destination_node is None:
            self.logger.debug("Destination node not cached. Will attempt to discover")
            # unpredictable behavior will result from duplicate NI's, the following picks the first
            destination_node = self.xnet.discover_device(dest_ip_NI)
            if destination_node is None:
                self.logger.debug("Unable to find destination node")
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
