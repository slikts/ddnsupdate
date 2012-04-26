#!/usr/bin/env python

import subprocess
import json

from config import client as config


def main(config):
    names = json.dumps(config.names)
    call_arg = ['/usr/bin/env', 'ssh', '-i%s' % config.ssh_key, config.ssh_host, names]
    config.logger.info(call_arg)
    subprocess.call(call_arg)


if __name__ == '__main__':
    main(config)