import sys
import logging
import signal
import time
from datetime import datetime
from radio import Radio
from tundevice import TunDevice
from xbeenet import XBeeNet
from utilities import setup_logging, config_setup, load_configs
from constants import APP_LOG

logger = logging.getLogger('Main')

def graceful_shutdown(net: XBeeNet, **args):
    logger.info("Starting graceful shutdown of XBeeNet")
    net.stop()
    start_time = time.time()
    while (net.is_alive()) or (time.time() < start_time + 5):
        time.sleep(.5)
    if net.is_alive():
        logger.critical("Unable to stop thread's running loop. Need to manually kill")
    else:
        datestamp = datetime.now().strftime('%Y%m%d %H:%M')
        with open(APP_LOG, 'a') as f:
            f.write(f'''\
###############################################
#              XBeeNet Stopped                #
#               {datestamp}                #
###############################################\n\
''')

def setup_signals(net: XBeeNet):
    signal.signal(signal.SIGINT, lambda *args: graceful_shutdown(net))
    signal.signal(signal.SIGTERM, lambda *args: graceful_shutdown(net))
    signal.signal(signal.SIGTSTP, lambda *args: graceful_shutdown(net))

def run_net():
    setup_logging()
    # check the platform
    if sys.platform != 'linux':
        logger.critical("Only compatible with the linux platform.")
        sys.exit(1)
    else:
        logger.debug("Linux platform detected. Starting up XBee Mesh network")
        
    # Read in configs
    config_setup()
    configs = load_configs()
    logger.info("Configs loaded")

    # Setup the XBeeNet Thread
    xbee_net = XBeeNet(configs)
    setup_signals(xbee_net)
    logger.info("Starting XBeeNet thread")
    xbee_net.start()
    xbee_net.join()
    xbee_net.stop()
    
if __name__ == '__main__':
    run_net()
