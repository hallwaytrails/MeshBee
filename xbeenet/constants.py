from enum import Enum

RADIO_LOGGER = 'Radio'
TUN_LOGGER = 'TunDevice'
NET_LOGGER = 'XBeeNet'

# CONFIG_DIR = '/etc/xbeenet'
CONFIG_DIR = '/tmp/xbeenet'
CONFIG_NAME = 'config.toml'

CONSOLE_LOGGER = True
DEFAULT_CONFIGS = 'default_configs.toml'

BAUDRATES = {
    1200:   0, 
    2400:   1, 
    4800:   2, 
    9600:   3, 
    19200:  4, 
    38400:  5, 
    57600:  6, 
    115200: 7, 
    230400: 8
}
