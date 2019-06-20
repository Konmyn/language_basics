# https://timber.io/blog/the-pythonic-guide-to-logging/
import logging

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.critical('logging is easier than I was expecting')
logger.critical("this better be bad")
logger.error("more serious problem")
logger.warning("an unexpected event")
logger.info("show user flow through program")
logger.debug("used to track variables when coding")
