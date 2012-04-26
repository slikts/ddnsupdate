logger = None
ttl = 90
wan_ip = None


def _update_config():
    from sys import getenv

    global logger, wan_ip

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    wan_ip = getenv('SSH_CONNECTION').split(' ')[0]


_update_config()
del _update_config

try:
    execfile('/etc/ddnsupdate/server.py')
except IOError:
    pass