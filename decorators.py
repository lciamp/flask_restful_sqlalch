import functools
from flask import abort


def db_check_or_return_500(func):
    @functools.wraps(func)
    def function_that_runs_func(*args, **kwargs):
        try:
            if func.__name__ == 'find_by_name':
                item = func(*args, **kwargs)
                return item
            else:
                func(*args, **kwargs)
        except:
            abort(500)
    return function_that_runs_func