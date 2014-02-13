import functools

def notify(dispatcher_class, event_factory_class, **kwargs):
    '''A decorator that notifies listeners about executed ckan API actions.
    
    This decorator should be applied to ckan API action functions which accept
    2 parameters: context and data_dict. It notifies the listeners after(if)
    the full body of the decorated function has been executed.
    
    :param dispatcher_class: a class with a classmethod *dispatch(events)*
    :param event_factory_class: a factory class for constructing events out of *data_dict*
        and any additional *kwargs*
    :param **kwargs: aditional arguments for the specified event factory class
    
    '''
    def actual_decorator(action_func):
        @functools.wraps(action_func)
        def wrapper(context, data_dict):
            result = action_func(context, data_dict)
            dispatcher_class.dispatch(event_factory_class.build_events(data_dict, **kwargs))
            return result
        return wrapper
    return actual_decorator
