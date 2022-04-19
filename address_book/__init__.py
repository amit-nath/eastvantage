import os
import logging

log_level = logging.INFO
if os.getenv('LOG_LEVEL', 'info') == 'debug':
    log_level = logging.DEBUG

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=log_level)
logger = logging.getLogger(__name__)
