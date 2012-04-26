ttl = 90
logger = None
wan_ip = None
zone = None
subzone = None
names = {}


def _update_config():
    import logging
    import json
    from sys import argv
    from os import getenv

    global logger, wan_ip, names, zone, subzone

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    wan_ip = getenv('SSH_CONNECTION').split(' ')[0]
    names = json.loads(getenv('SSH_ORIGINAL_COMMAND'))
    zone = argv[1]
    if len(argv) > 2:
        subzone = argv[2]



_update_config()
del _update_config

try:
    execfile('/etc/ddnsupdate/server.py')
except IOError:
    pass