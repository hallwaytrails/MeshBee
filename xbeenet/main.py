import sys, logging
from radio import Radio
from tundevice import TunDevice
from utilities import setup_loggers, config_setup, load_configs

setup_loggers()
logger = logging.getLogger('XBeeNet')

if sys.platform != 'linux':
    logger.critical("Only compatible with the linux platform.")
    sys.exit(1)
else:
    logger.info("Linux platform detected. Starting up XBee Mesh network")

# Read in configs
config_setup()
configs = load_configs()
config_ip = configs['net']['ip']
config_port = configs['radio']['port']
config_baud = configs['radio']['baud']
xbee = Radio(ip = config_ip, port = config_port, baud = config_baud)
# tun = TunDevice()

# # main event loop
# while True:
#     packet = tun.poll(10)
#     if packet is not None:
#         xbee.tx(packet['IP'], packet['payload'])
#     packet = xbee.poll()
#     if packet is not None:
#         tun.tx(packet)
