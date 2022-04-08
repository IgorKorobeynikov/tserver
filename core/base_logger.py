import logging

logger = logging.getLogger('SERVER')
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('dbg.log')
fileHandler.setLevel(logging.NOTSET)

logger.addHandler(fileHandler)

formatter = logging.Formatter('[%(asctime)s]-<%(name)s>-<%(levelname)s> - %(message)s')
fileHandler.setFormatter(formatter)
