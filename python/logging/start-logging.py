# https://timber.io/blog/the-pythonic-guide-to-logging/
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logPath = BASE_DIR
fileName = "myLogs"
print(logPath)
print(fileName)


logger = logging.getLogger(__name__)

# console logger
# logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=logFormatter, level=logging.DEBUG)

# filelogger
# handler = logging.FileHandler('myLogs.log')
# handler.setLevel(logging.INFO)
# logger.addHandler(handler)

# console and file logger #1
# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()
#
# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)
#
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

# console and file logger #2
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)-8.8s][%(name)s:%(lineno)d]-> %(message)s',
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
        logging.StreamHandler()
    ])

logger.critical('logging is easier than I was expecting')
logger.critical("this better be bad")
logger.error("more serious problem")
logger.warning("an unexpected event")
logger.info("show user flow through program")
logger.debug("used to track variables when coding")
