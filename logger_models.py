import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

file_handler = logging.FileHandler('model_parts.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
