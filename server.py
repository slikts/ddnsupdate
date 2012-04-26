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
    subgroup_pattern = re.compile(r'^[*\w\d]+$')
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
                    print subgroup
                    exit()
                    raise cls.InvalidCharacters

    def __init__(self, config):
        self.config = config
        config.logger.info('Zone: %s' % config.zone)
        config.logger.info('Subzone: %s' % config.subzone)

    def update(self):
        commands = []
        params = {
            'wan_ip': self.config.wan_ip
        }
        for name, (value, record_type) in self.config.names.iteritems():
            config = self.config
            name_zone = config.zone
            if config.subzone:
                name_zone = '%s.%s' % (config.subzone, name_zone)
            name = '%s%s' % (self.clean_name(name), name_zone)
            self.validate_name(name)
            value = value % params
            commands += ['update delete %s %s' % (name, record_type),
            'update add %s. %d %s %s' % (name, config.ttl, record_type, value)]
        self._run(commands)

    def _run(self, commands):
        commands = ['zone %s' % (self.config.zone)] \
            + commands + ['send\n']
        handle, pathname = tempfile.mkstemp(text=True)
        descriptor = os.fdopen(handle, 'w')
        descriptor.write('\n'.join(commands))
        descriptor.close()
        self.config.logger.info('Input file: %s' % pathname)
        for command in commands:
            self.config.logger.info('Command: %s' % command)
        subprocess.call(['/usr/bin/env', 'nsupdate', '-l', pathname])
        os.unlink(pathname)


def main():
    from config import server as config
    server = DDNS(config)
    server.update()


if __name__ == '__main__':
    main()