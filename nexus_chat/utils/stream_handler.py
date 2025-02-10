"""Stream handler module."""
import asyncio
import logging
from typing import Optional

from ..gui.chat_window import ChatBubble

logger = logging.getLogger(__name__)

class ResponseStream:
    """Response stream handler."""
    
    def __init__(self, chat_bubble: ChatBubble):
        """Initialize stream handler."""
        self.chat_bubble = chat_bubble
        self.buffer = ""
        self.update_interval = 0.05  # 50ms
        self.buffer_size = 10  # caracteres
        self.last_update = 0
        
    async def process_chunk(self, chunk: str):
        """Process response chunk."""
        try:
            # Add to buffer
            self.buffer += chunk
            
            # Check if should update
            current_time = asyncio.get_event_loop().time()
            should_update = (
                len(self.buffer) >= self.buffer_size or
                (current_time - self.last_update) >= self.update_interval
            )
            
            if should_update:
                await self.flush()
                
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
            raise
            
    async def flush(self):
        """Flush buffer to chat bubble."""
        try:
            if self.buffer:
                # Update chat bubble
                self.chat_bubble.update_content(self.buffer)
                
                # Reset buffer
                self.buffer = ""
                
                # Update timestamp
                self.last_update = asyncio.get_event_loop().time()
                
        except Exception as e:
            logger.error(f"Error flushing buffer: {e}")
            raise
