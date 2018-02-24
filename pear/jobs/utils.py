# coding=utf-8

def import_module_by_str(module_name):
    if isinstance(module_name, unicode):
        module_name = str(module_name)
    __import__(module_name)
