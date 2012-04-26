ssh_host = None
ssh_key = None
logger = None
names = {}


def _update_config():
    import logging

    global logger
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()


_update_config()
del _update_config

try:
    execfile('/etc/ddnsupdate/client.py')
except IOError:
    pass