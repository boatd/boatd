from __future__ import print_function

import time

VERBOSE, NORMAL, WARN, ERROR = range(4)


def color(message, text_color, text_style=0):
    return '\033[{};{}m{}\033[0m'.format(text_style, text_color, message)

def log(message, level=NORMAL):
    print(time.strftime('[%H:%M:%S]'), message)
