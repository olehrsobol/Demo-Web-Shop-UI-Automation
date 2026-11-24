import functools
import inspect
import allure


def step(title: str):
    def decorator(func):
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()

            with allure.step(title.format(**bound.arguments)):
                return func(*args, **kwargs)

        return wrapper
    return decorator
