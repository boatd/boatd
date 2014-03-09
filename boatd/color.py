def color(message, text_color, text_style=0):
    '''Return the message wrapped in ansi color code'''
    return '\033[{};{}m{}\033[0m'.format(text_style, text_color, message)
