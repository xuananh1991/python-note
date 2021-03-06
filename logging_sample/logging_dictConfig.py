from logging.config import dictConfig
import logging
import os
import json

# with open('/home/xuananh/Dropbox/Work/Other/slack-token-api-key.json', "r") as in_file:
#     SLACK_API_KEY = json.load(in_file)['phungxuananh']

# LOGGING_SLACK_API_KEY = SLACK_API_KEY
# LOGGING_SLACK_CHANNEL = "#general"

class MyFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg
        
        if allow:
            record.msg = 'changed: ' + record.msg
        
        return allow

LOG_DIR = 'logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'add_my_custom_attribute': {
            '()': 'formatter.custom_format.MyCustomFormatAttributes',
        },
        'myfilter': {
            '()': MyFilter,
            'param': 'noshow',
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] [%(custom_format)s] [%(name)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['add_my_custom_attribute', 'myfilter']
        },
        'app.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.log',
            'maxBytes': 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
            'filters': ['add_my_custom_attribute']
        },
        'app.ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.ERROR.log',
            'maxBytes': 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
            'filters': ['add_my_custom_attribute']
        },
        # 'slack.ERROR': {
        #     'level': 'ERROR',
        #     'api_key': LOGGING_SLACK_API_KEY,
        #     'class': 'slacker_log_handler.SlackerLogHandler',
        #     'channel': LOGGING_SLACK_CHANNEL
        # },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'app.DEBUG', 'app.ERROR'],
            'propagate': False,
            'level': 'INFO',
        },
    }
}

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

dictConfig(LOGGING)

# list all logger
print('--------------------------------------------------------')
print(logging.Logger.manager.loggerDict)
print('--------------------------------------------------------')

logger = logging.getLogger('app')

logger.error('aaaaaaaaaaaaaaaaaaa')
logger.info('aaaaaaaaaaaaaaaaaaa')

logger.error('hello')
logger.error('hello - noshow')