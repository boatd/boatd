import os


def reldir(file, name):
    '''Return a path to a directory in the same directory as file'''

    path, _ = os.path.split(file)

    return os.path.join(path, name)
