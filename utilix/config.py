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

    def __init__(self, path=None):
        if not Config.instance:
            Config.instance = Config.__Config(path=path)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Config(configparser.ConfigParser):

        def __init__(self, path=None):

            if 'XENON_CONFIG' not in os.environ:
                logger.warning('$XENON_CONFIG is not defined in the environment')
            if 'HOME' not in os.environ:
                logger.warning('$HOME is not defined in the environment')
            home_config = os.path.join(os.environ['HOME'], '.xenon_config')
            xenon_config = os.environ.get('XENON_CONFIG')

            # if path is passed, use that
            if path:
                config_file_path = path

            # if not, see if there is a XENON_CONFIG environment variable
            elif xenon_config:
                config_file_path = os.environ.get('XENON_CONFIG')

            # if not, then look for hidden file in HOME
            elif os.path.exists(os.path.join(os.environ['HOME'], '.xenon_config')):
                config_file_path = home_config

            logger.debug('Loading configuration from %s' % (config_file_path))
            configparser.ConfigParser.__init__(self, interpolation=EnvInterpolation())

            self.config_path = config_file_path

            try:
                self.read_file(open(config_file_path), 'r')
            except FileNotFoundError as e:
                raise RuntimeError(
                    'Unable to open %s. Please see the README for an example configuration' % (config_file_path)) from e

        def get_list(self, category, key):
            list_string = self.get(category, key)
            return [s.strip() for s in list_string.split(',')]
