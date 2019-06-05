#!/usr/bin/env python
import logging
import getopt
import sys
import time
import random

def main(argv):
    logFile = 'random.log'
    logPattern = '%(asctime)s,%(msecs)d %(process)d %(filename)s %(lineno)d %(name)s %(levelname)s %(message)s'
    datePattern = "%Y-%m-%d %H:%M:%S"

    # setup logging
    logging.Formatter.converter = time.gmtime
    logger = logging.getLogger("log-generator")
    logger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(logPattern,datePattern)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    before = time.time()
    # when set to 10**6, file size is 156M, and time cost 20s in my vm, 30s in user machine
    for i in range(10**6):
        logger.debug("%0100d" % i)
    after = time.time()
    print(after-before)

    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
