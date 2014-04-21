from __future__ import print_function

import os
import time

from .color import color

class GpxLogger(object):
    def __init__(self, boat, base_filename):
        self.log_dir, self.log_name = os.path.split(base_filename)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)


VERBOSE, NORMAL, WARN, ERROR = range(4)


def log(message, level=NORMAL):
    messages = []
    if level > WARN:
        text = 'WARNING'
        if level == ERROR:
            text = 'ERROR'
        messages.append('[{}]'.format(color(text, 31)))

    messages.append(message)
    print(time.strftime('[%H:%M:%S]'), *messages)
