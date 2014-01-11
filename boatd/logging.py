from __future__ import print_function

import time

NORMAL, SUCCESS, WARN, ERROR = range(4)

def log(message):
    print(time.strftime('[%H:%M:%S]'), message)
