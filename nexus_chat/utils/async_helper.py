"""Async helper module."""
import asyncio
import functools
import logging
from typing import Any, Callable, Coroutine, Optional

logger = logging.getLogger(__name__)

def async_handler(func: Callable) -> Callable:
    """Decorator for handling async functions in tkinter.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        try:
            # Get self from args
            self = args[0]
            
            # Get async helper
            async_helper = getattr(self, "async_helper", None)
            if not async_helper:
                raise ValueError("No async helper found")
                
            # Run coroutine
            return async_helper.run_coroutine(func(*args, **kwargs))
            
        except Exception as e:
            logger.error(f"Error in async handler: {str(e)}")
            raise
            
    return wrapper

class AsyncHelper:
    """Helper class for running async code in tkinter."""
    
    def __init__(self):
        """Initialize async helper."""
        try:
            logger.info("Initializing async helper")
            
            # Create event loop
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # Create tasks list
            self.tasks = []
            
            logger.info("Async helper initialized")
            
        except Exception as e:
            logger.error(f"Error initializing async helper: {str(e)}")
            raise
            
    def run_coroutine(self, coroutine: Coroutine) -> Any:
        """Run coroutine in event loop.
        
        Args:
            coroutine: Coroutine to run
            
        Returns:
            Result of coroutine
        """
        try:
            # Create task
            task = self.loop.create_task(coroutine)
            self.tasks.append(task)
            
            # Run task
            return self.loop.run_until_complete(task)
            
        except Exception as e:
            logger.error(f"Error running coroutine: {str(e)}")
            raise
            
    def run_callback(self, callback: Callable, *args, **kwargs):
        """Run callback in event loop.
        
        Args:
            callback: Callback to run
            args: Positional arguments
            kwargs: Keyword arguments
        """
        try:
            # Create coroutine
            async def _run_callback():
                return callback(*args, **kwargs)
                
            # Run coroutine
            self.run_coroutine(_run_callback())
            
        except Exception as e:
            logger.error(f"Error running callback: {str(e)}")
            raise
            
    async def close(self):
        """Close event loop."""
        try:
            # Cancel tasks
            for task in self.tasks:
                task.cancel()
                
            # Wait for tasks
            await asyncio.gather(*self.tasks, return_exceptions=True)
            
            # Close loop
            self.loop.close()
            
            logger.info("Async helper closed")
            
        except Exception as e:
            logger.error(f"Error closing async helper: {str(e)}")
            raise
