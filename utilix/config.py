import os
import configparser
import logging

logger = logging.getLogger("utilix")

# copy + pasted from outsource.Config

class EnvInterpolation(configparser.BasicInterpolation):
    '''Interpolation which expands environment variables in values.'''

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


class Config():
    # singleton
    instance = None

    def __init__(self):
        if not Config.instance:
            Config.instance = Config.__Config()
    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Config(configparser.ConfigParser):

        def __init__(self):
            config_file_path = os.path.join(os.environ['HOME'], '.xenonnt.conf')
            logger.debug('Loading configuration from %s' % (config_file_path))
            configparser.ConfigParser.__init__(self, interpolation=EnvInterpolation())

            try:
                self.read_file(open(config_file_path), 'r')
            except FileNotFoundError as e:
                raise RuntimeError(
                    'Unable to open %s. Please see the README for an example configuration' % (config_file_path)) from e
