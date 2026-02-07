import logging
from functools import wraps

logger = logging.getLogger(__name__)

def logger_calls(func):
    """Декоратор для логирования вызовов функций"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
            
    return wrapper