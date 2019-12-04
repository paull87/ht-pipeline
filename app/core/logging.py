import logging
import sys
import inspect

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_format = logging.Formatter('%(asctime)s - %(filename)s.%(funcName)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_format)

logger.addHandler(stream_handler)
