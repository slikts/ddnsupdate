#!/usr/bin/env python

import os
import re
import tempfile
import subprocess


class DDNS(object):
    max_name_len = 255
    max_group_len = 63
    group_sep = '.'
    subgroup_sep = '-'
    subgroup_pattern = re.compile(r'\w\d')
    config = None
    
    class NameTooLong(Exception):
        pass

    class GroupTooLong(Exception):
        pass

    class InvalidCharacters(Exception):
        pass

    @staticmethod
    def clean_name(name):
        return name.strip().lower()

    @classmethod
    def validate_name(cls, name):
        if len(name) > cls.max_name_len:
            raise cls.NameTooLong
        for group in name.split(cls.group_sep):
            if len(group) > cls.max_group_len:
                raise cls.GroupTooLong
            for subgroup in group.split(cls.subgroup_sep):
                if not cls.subgroup_pattern.match(subgroup):
                    raise cls.InvalidCharacters

    def __init__(self, config):
        self.config = config

    def update(self):
        commands = []
        for name, value in self.config.names.iteritems():
            name = self.clean_name(name)
            self.validate_name(name)
            value = value % self.config
            commands += ['update delete %s' % name,
            'update add %s. %d A' (name, config.ttl)]
        tmp = tempfile.mkstemp(text=True)
        tmp.write('\n'.join(commands))
        tmp.close()
        logger.debug('Input file: %s')
        for command in commands:
            logger.info('Command: %s' % command)
        subprocess.call(['/usr/bin/env', 'nsupdate', f.name])
        os.unlink(tmp.name)


def main():
    from config import server as config
    server = DDNS(config)
    server.update()


if __name__ == '__main__':
    main()