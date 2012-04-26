logger = None
ttl = 90
wan_ip = None
names = {}


def _update_config():
    import logging
    import json
    from os import getenv

    global logger, wan_ip, names

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    wan_ip = getenv('SSH_CONNECTION').split(' ')[0]

    names = json.loads(getenv('SSH_ORIGINAL_COMMAND'))


_update_config()
del _update_config

try:
    execfile('/etc/ddnsupdate/server.py')
except IOError:
    pass