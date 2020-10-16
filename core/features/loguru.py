from loguru import logger
from functools import wraps

def loguru_info(func) -> object:
    def new_func(*args, **kwargs):
        func_name = func.__name__

        logger.info(f"Called method - {func_name}")
        try:
            return func(*args, *kwargs)
        except Exception as exception:
            logger.warning(f"Was called {exception.__class__.__name__} in {func_name}")
            raise exception
    return new_func()
