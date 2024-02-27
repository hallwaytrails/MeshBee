############################################################################
# 
#  File: constants.py
#  Copyright(c) 2023, Hallway Trails LLC. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

from enum import Enum

CONFIG_DIR = '/etc/meshnet'
CONFIG_NAME = 'config.toml'

APP_LOG_DIR = '/var/log'
APP_LOG = f'{APP_LOG_DIR}/meshnet.log'

class LoggerNames(str, Enum):
    MAIN =  "Main"
    RADIO = "Radio"
    TUN =   "TunDevice"
    NET =   "XBeeNet"
    GUI =   "Gui"

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
