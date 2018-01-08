import yaml
import os

class ConfigParser:

    config_file = os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'
    config_vars = None

    def __init__(self):
        self.config_vars = yaml.load(open(self.config_file,'r'))

    @classmethod
    def get(cls, server, key=None):
        if not cls.config_vars:
            cls.config_vars = yaml.load(open(cls.config_file, 'r'))

        section = cls.config_vars.get(server, None)
        if section is None:
            raise NotImplementedError

        if key is None:
            return section

        value = section.get(key, None)
        if value is None:
            raise NotImplementedError

        return value