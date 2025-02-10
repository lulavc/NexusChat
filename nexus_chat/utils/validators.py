import logging
from functools import wraps

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

def validate_input(*validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                for validator in validators:
                    validator(self)
                return func(*args, **kwargs)
            except ValidationError as e:
                logger.error(f'Validation failed: {e}')
                if hasattr(self, 'show_error'):
                    self.show_error(str(e))
                else:
                    raise
        return wrapper
    return decorator
