from __future__ import print_function

import time

VERBOSE, NORMAL, WARN, ERROR = range(4)


def log(message, level=NORMAL):
    print(time.strftime('[%H:%M:%S]'), message)
