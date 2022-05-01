import logging
import logging.handlers

logger = logging.getLogger('SERVER')
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('dbg.log')
fileHandler.setLevel(logging.DEBUG)
bufferHandler = logging.handlers.BufferingHandler(100)
bufferHandler.setLevel(logging.DEBUG)

logger.addHandler(fileHandler)
logger.addHandler(bufferHandler)

formatter = logging.Formatter('[%(asctime)s]-<%(name)s>-<%(levelname)s> - %(message)s')
fileHandler.setFormatter(formatter)
bufferHandler.setFormatter(formatter)
