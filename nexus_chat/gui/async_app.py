"""Async application wrapper for CTk."""
import asyncio
import threading
from queue import Queue
from typing import Any, Callable, Optional
import customtkinter as ctk

class AsyncApp:
    """Wrapper for running async code with CTk."""
    
    def __init__(self):
        """Initialize async app."""
        self.loop = asyncio.new_event_loop()
        self.call_queue = Queue()
        self.running = False
        self._start_thread()
    
    def _start_thread(self):
        """Start the async thread."""
        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.running = True
            self.loop.run_forever()
        
        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the async app."""
        self.running = False
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
    
    def process_queue(self):
        """Process callbacks from async thread."""
        while not self.call_queue.empty():
            callback, args, kwargs = self.call_queue.get_nowait()
            callback(*args, **kwargs)
    
    def schedule_callback(self, callback: Callable, *args: Any, **kwargs: Any):
        """Schedule a callback to be run in the main thread."""
        self.call_queue.put((callback, args, kwargs))
    
    def create_task(self, coro, callback: Optional[Callable] = None):
        """Create a task in the async loop with optional callback."""
        async def wrapped():
            try:
                result = await coro
                if callback:
                    self.schedule_callback(callback, result)
            except Exception as e:
                if callback:
                    self.schedule_callback(callback, None, e)
                else:
                    raise
        
        return asyncio.run_coroutine_threadsafe(wrapped(), self.loop)

class AsyncTk(ctk.CTk):
    """CTk with async support."""
    
    def __init__(self, *args, **kwargs):
        """Initialize async window."""
        super().__init__(*args, **kwargs)
        self.async_app = AsyncApp()
        self._setup_queue_handler()
    
    def _setup_queue_handler(self):
        """Setup periodic queue check."""
        def check_queue():
            self.async_app.process_queue()
            self.after(10, check_queue)
        check_queue()
    
    def destroy(self):
        """Clean up async resources."""
        self.async_app.stop()
        super().destroy()
    
    def create_task(self, coro, callback: Optional[Callable] = None):
        """Create an async task."""
        return self.async_app.create_task(coro, callback)
