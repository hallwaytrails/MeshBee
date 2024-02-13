import os, sys, logging
from xbeenet.radio import Radio
# import backend_pytun
# import backend_wintap

# backend = None

# logging.basicConfig(level=logging.DEBUG)

# if os.name == 'posix':
#     logging.debug('OS is posix, using python-pytun to network.')
#     backend = backend_pytun.backend()
# else:
#     sys.exit('Unsupported os: ' + os.name)

xbee = Radio

# event loop
while True:
    packet = backend.poll(10)
    if packet is not None:
        xbee.tx(packet['IP'], packet['payload'])
    packet = xbee.poll()
    if packet is not None:
        backend.tx(packet)
