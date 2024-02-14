import logging
import pkgutil
import tomlkit
from pathlib import Path
from datetime import datetime
from constants import CONSOLE_LOGGER, CONFIG_DIR, CONFIG_NAME, DEFAULT_CONFIGS

def setup_loggers():
    radio_formatter = logging.Formatter('{asctime} - {name:10s} - {levelname:8s} - {message}', '%Y%m%d-%H:%M:%S', style='{')
    tun_formatter = logging.Formatter('{asctime} - {name:10s} - {levelname:8s} - {filename}:{lineno} - {message}', '%Y%m%d-%H:%M:%S', style='{')
    net_formatter = logging.Formatter('{asctime} - {name:10s} - {levelname:8s} - {message}', '%Y%m%d-%H:%M:%S', style='{')

    # pyfldm_file_handler = logging.FileHandler(APP_LOG)
    # pyfldm_file_handler.setLevel(logging.DEBUG)
    # pyfldm_file_handler.setFormatter(pyfldm_formatter)

    # basestation_file_handler = logging.FileHandler(APP_LOG)
    # basestation_file_handler.setLevel(logging.DEBUG)
    # basestation_file_handler.setFormatter(basestation_formatter)

    datestamp = datetime.now().strftime('%Y%m%d-%H%M')
    # tx_file_handler = logging.FileHandler(f'{TX_LOG_DIR}/{datestamp}_basestation_tx.log')
    # tx_file_handler.setLevel(logging.DEBUG)
    # tx_file_handler.setFormatter(tx_formatter)

    radio_logger = logging.getLogger('Radio')
    radio_logger.setLevel(logging.DEBUG)
    # pyfldm_logger.addHandler(pyfldm_file_handler)

    tun_logger = logging.getLogger('BaseStation')
    tun_logger.setLevel(logging.DEBUG)
    # tun_logger.addHandler(basestation_file_handler)

    net_logger = logging.getLogger('XBeeNet')
    net_logger.setLevel(logging.DEBUG)
    # net_logger.addHandler(tx_file_handler)

    if CONSOLE_LOGGER:
        console_handler1 = logging.StreamHandler()
        console_handler1.setLevel(logging.DEBUG)
        console_handler1.setFormatter(radio_formatter)
        radio_logger.addHandler(console_handler1)
    
        console_handler2 = logging.StreamHandler()
        console_handler2.setLevel(logging.DEBUG)
        console_handler2.setFormatter(tun_formatter)
        tun_logger.addHandler(console_handler2)

        console_handler3 = logging.StreamHandler()
        console_handler3.setLevel(logging.DEBUG)
        console_handler3.setFormatter(net_formatter)
        net_logger.addHandler(console_handler3)

#     datestamp = datetime.now().strftime('%Y%m%d %H:%M')
#     with open(APP_LOG, 'a') as f:
#         f.write(f'''\
# ###############################################
# #        Starting GRC-137 Base Station        #
# #               {datestamp}                #
# ###############################################\n\
# ''')
        
def config_setup():
    if not Path(CONFIG_DIR).exists():
        Path(CONFIG_DIR).mkdir(exist_ok=True)
    if not Path(f'{CONFIG_DIR}/{CONFIG_NAME}').exists():
        config_bin = pkgutil.get_data('configs', DEFAULT_CONFIGS)
        with open(f'{CONFIG_DIR}/{CONFIG_NAME}', 'wb') as f:
            f.write(config_bin)

def load_configs():
    configs = None
    # read in configs
    with open(f'{CONFIG_DIR}/{CONFIG_NAME}', mode="rt") as fp:
        configs = tomlkit.load(fp)
    return configs