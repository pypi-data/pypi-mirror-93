import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(log_color)s%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
date_format = '%Y-%m-%d %H:%M:%S'
logging.root.setLevel(LOG_LEVEL)

colors = {
    'DEBUG': 'bold_green',
    'INFO': 'bold_blue',
    'WARNING': 'bold_purple',
    'ERROR': 'bold_yellow',
    'CRITICAL': 'bold_red'
}

formatter = ColoredFormatter(LOGFORMAT, date_format, log_colors=colors)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)
