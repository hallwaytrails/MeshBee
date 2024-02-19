from enum import Enum

RADIO_LOGGER = 'Radio'
TUN_LOGGER = 'TunDevice'
NET_LOGGER = 'XBeeNet'

CONFIG_DIR = '/etc/xbeenet'
# CONFIG_DIR = '/tmp/xbeenet'
CONFIG_NAME = 'config.toml'

APP_LOG_DIR = '/var/xbeenet'
APP_LOG = f'{APP_LOG_DIR}/app.log'
LOGGER_NAMES = (
    'Main',
    'XBeeNet',
    'Radio',
    'TunDevice'
)

CONSOLE_LOGGER = True
DEFAULT_CONFIGS = 'default_configs.toml'
DEFAULT_MTU = 256

# Putting a few values out of order to test common values first, reduces discovery time
BAUDRATES = {
    9600:   3,
    230400: 8,
    1200:   0, 
    2400:   1, 
    4800:   2, 
    19200:  4, 
    38400:  5, 
    57600:  6, 
    115200: 7
}
