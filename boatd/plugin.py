import os
import imp

def get_module_name(filepath):
    _, name = os.path.split(filepath)
    module_name, _ = os.path.splitext(name)
    return module_name

def find_plugins(search_directories):
    found_plugins = []
    for directory in search_directories:
        for plugin in os.listdir(directory):
            if plugin.endswith('.py'):
                found_plugins.append(os.path.join(directory, plugin))

    return found_plugins
