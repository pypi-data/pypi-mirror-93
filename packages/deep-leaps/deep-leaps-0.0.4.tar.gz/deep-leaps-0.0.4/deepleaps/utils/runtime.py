from importlib import import_module
import sys

def get_instance_from_name(module_path, class_name, *args, **kwargs):
    m = import_module(module_path)
    return getattr(m, class_name)(*args, **kwargs)

def get_class_object_from_name(module_path, class_name):
    m = import_module(module_path)
    return getattr(m, class_name)

def load_module(module):
    # module_path = "mypackage.%s" % module
    module_path = module
    if module_path in sys.modules:
        return sys.modules[module_path]
    return __import__(module_path, fromlist=[module])
