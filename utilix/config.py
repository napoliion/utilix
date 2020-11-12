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
            Config.instance = Config.__Config()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Config(configparser.ConfigParser):

        def __init__(self):

            if 'XENON_CONFIG' not in os.environ:
                logger.info('$XENON_CONFIG is not defined in the environment')
            if 'HOME' not in os.environ:
                logger.warning('$HOME is not defined in the environment')
            home_config = os.path.join(os.environ['HOME'], '.xenon_config')
            xenon_config = os.environ.get('XENON_CONFIG')

            # if not, see if there is a XENON_CONFIG environment variable
            if xenon_config:
                config_file_path = os.environ.get('XENON_CONFIG')

            # if not, then look for hidden file in HOME
            elif os.path.exists(home_config):
                config_file_path = home_config

            else:
                raise FileNotFoundError(f"Could not load a configuration file. "
                                        f"You can create one at {home_config}, or set a custom path using\n\n"
                                        f"export XENON_CONFIG=path/to/your/config\n")

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
