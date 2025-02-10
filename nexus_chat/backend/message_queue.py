"""Message queue for handling chat messages."""
import asyncio
from typing import Optional
from models.message import Message

class MessageQueue:
    """Handles queueing and processing of chat messages."""
    
    def __init__(self):
        """Initialize the message queue."""
        self.queue: asyncio.Queue[Message] = asyncio.Queue()
        self._processing = False
        self._task: Optional[asyncio.Task] = None
    
    async def put(self, message: Message) -> None:
        """Add a message to the queue."""
        await self.queue.put(message)
        if not self._processing:
            self._start_processing()
    
    def _start_processing(self) -> None:
        """Start processing messages in the queue."""
        if not self._task or self._task.done():
            self._processing = True
            self._task = asyncio.create_task(self._process_queue())
    
    async def _process_queue(self) -> None:
        """Process messages in the queue."""
        try:
            while not self.queue.empty():
                message = await self.queue.get()
                # Process message (e.g., save to history, update UI)
                self.queue.task_done()
        finally:
            self._processing = False
