import imp
import os
import threading

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

def load_plugins(*plugin_names):
    modules = []
    for module_filename in plugin_names:
        with open(module_filename) as f:
            module = imp.load_module(
                get_module_name(module_filename),
                f,
                module_filename,
                ('.py', 'U', 1)
            )
            modules.append(module)

    return modules

def start_plugins(modules, passed_args):
    for module in modules:
        thread = threading.Thread(target=module.plugin_main,
                                  args=tuple(passed_args))
        thread.start()
