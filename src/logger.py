__author__ = 'gbaranowski'

from logging.config import dictConfig
from os import path, makedirs

location = path.split(path.dirname(path.realpath(__file__)))[0]
location = path.join(location, 'logs')
try:
    makedirs(location)
except OSError:
    if not path.isdir(location):
        raise

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

        'simple': {
            'format': '[%(levelname)s] : %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'persistant': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': path.join(location, 'log'),
            'backupCount': 10,
        },
    },

    'loggers': {
        '': {
            'handlers': ['default', 'persistant'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def start_logging(ll, lfl, ltl):
    logging_config['loggers']['']['level'] = ll
    logging_config['handlers']['default']['level'] = ltl
    logging_config['handlers']['persistant']['level'] = lfl
    dictConfig(logging_config)
