"""
Error handling utilities
"""
import logging
import traceback
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('SatyaAI')


def handle_errors(func):
    """
    Decorator to handle errors gracefully.
    
    Usage:
        @handle_errors
        def my_function():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper


def log_operation(operation_name):
    """
    Decorator to log operations.
    
    Usage:
        @log_operation("store_claim")
        def store_claim(...):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Starting: {operation_name}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Completed: {operation_name}")
                return result
            except Exception as e:
                logger.error(f"Failed: {operation_name} - {str(e)}")
                raise
        return wrapper
    return decorator


class SatyaAIException(Exception):
    """Base exception for SatyaAI"""
    pass


class EmbeddingError(SatyaAIException):
    """Error during embedding generation"""
    pass


class StorageError(SatyaAIException):
    """Error during storage operations"""
    pass


class SearchError(SatyaAIException):
    """Error during search operations"""
    pass


class ValidationError(SatyaAIException):
    """Error during validation"""
    pass