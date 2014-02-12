import functools

def notify(dispatcher_class, event_class):
    '''A decorator that notifies listeners about executed ckan API actions.
    
    This decorator should be applied to ckan API action functions which accept
    2 parameters: context and data_dict. It notifies the listeners after(if)
    the full body of the decorated function has been executed.
    
    :param dispatcher_class: a class with a classmethod *dispatch(event)*
    :param event_class: a class for constructing events out of *data_dict*
    
    '''
    def actual_decorator(action_func):
        @functools.wraps(action_func)
        def wrapper(context, data_dict):
            result = action_func(context, data_dict)
            dispatcher_class.dispatch(event_class(data_dict))
            return result
        return wrapper
    return actual_decorator