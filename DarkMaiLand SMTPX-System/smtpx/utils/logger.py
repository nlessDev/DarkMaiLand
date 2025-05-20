import logging
import logging.config
import os

def setup_logging():
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf')
    logging.config.fileConfig(config_file)
    return logging.getLogger('smtpx')

logger = setup_logging()
