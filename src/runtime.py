import sys

def hook_module_function(module, function_name, replacement_function):
    ''' Hooks a function in designated module.
    
    function with function_name in specified module will be replaced with
    replacement_function. replacement_function should accept original
    function object plus the same arguments that original function accepts.
    
    module can be a module name, which must then be importable, or a
    module object.
    '''
    
    if isinstance(module, basestring):
        __import__(module)
        module = sys.modules[module]
    function = getattr(module, function_name)
    def hooked(*args, **kwargs):
        return replacement_function(function, *args, **kwargs)
    setattr(module, function_name, hooked)
