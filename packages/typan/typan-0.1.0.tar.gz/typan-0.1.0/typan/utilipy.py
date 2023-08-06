import functools

def repeat(amount=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            if amount != None:
                for _ in range(amount):
                    value = func(*args,**kwargs)
            else:
                for _ in range(2):
                    value = func(*args,**kwargs)
            return value
        return wrapper
    return decorator