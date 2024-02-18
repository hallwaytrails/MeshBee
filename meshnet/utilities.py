import logging
import pkgutil
import tomlkit
from pathlib import Path
from datetime import datetime
from constants import CONSOLE_LOGGER, CONFIG_DIR, CONFIG_NAME, DEFAULT_CONFIGS, \
    APP_LOG, APP_LOG_DIR, LOGGER_NAMES

def setup_logging():
    if not Path(APP_LOG_DIR).exists():
        Path(APP_LOG_DIR).mkdir(exist_ok=True)
    for name in LOGGER_NAMES:
        setup_logger(name)
    datestamp = datetime.now().strftime('%Y%m%d %H:%M')
    with open(APP_LOG, 'a') as f:
        f.write(f'''\
###############################################
#              Starting XBeeNet               #
#               {datestamp}                #
###############################################\n\
''')
    
def setup_logger(logger_name):
    formatter = logging.Formatter('{asctime} - {name:10s} - {levelname:8s} - {filename}:{lineno} - {message}', '%Y%m%d-%H:%M:%S', style='{')

    file_handler = logging.FileHandler(APP_LOG)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    if CONSOLE_LOGGER:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
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