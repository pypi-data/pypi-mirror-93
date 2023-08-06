import os
import configparser
import logging

logger = logging.getLogger("utilix")


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
                if 'USERPROFILE' in os.environ:
                    # Are you on windows?
                    home_config = os.path.join(os.environ['USERPROFILE'], '.xenon_config')
                else:
                    logger.warning('USERPROFILE is not defined in the environment')
            else:
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

        @property
        def logging_level(self):
            # look for logging level in 'basic'  field in config file. Defaults to WARNING
            level = self.get('basic', 'logging_level', fallback='WARNING').upper()
            possible_levels = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if level not in possible_levels:
                raise RuntimeError(f"The logging level {level} is not valid. "
                                   f"Available levels are: \n{possible_levels}.\n "
                                   f"Please modify {self.config_path}")
            return level
