"""Chat bubble module."""
import logging

import customtkinter as ctk

from nexus_chat.models.message import Message, MessageRole
from nexus_chat.utils.constants import GUI_CONSTANTS

logger = logging.getLogger(__name__)

class ChatBubble(ctk.CTkFrame):
    """Chat bubble widget."""
    
    def __init__(self, master, message: Message, fg_color: str = None):
        """Initialize chat bubble."""
        try:
            # Initialize parent
            if fg_color is None:
                if message.role == MessageRole.USER:
                    fg_color = GUI_CONSTANTS["USER_COLOR"]
                elif message.role == MessageRole.ASSISTANT:
                    fg_color = GUI_CONSTANTS["ASSISTANT_COLOR"]
                else:
                    fg_color = GUI_CONSTANTS["SYSTEM_COLOR"]
                    
            super().__init__(master, fg_color=fg_color)
            
            # Store message
            self.message = message
            self.content = ""
            
            # Create widgets
            self._create_widgets()
            
            # Configure grid
            self._configure_grid()
            
            # Update content
            self.update_content(message.content)
            
        except Exception as e:
            logger.error(f"Error initializing chat bubble: {e}")
            raise
            
    def _create_widgets(self):
        """Create widgets."""
        try:
            # Create text widget
            self.text_widget = ctk.CTkTextbox(
                self,
                wrap="word",
                fg_color=self.cget("fg_color"),
                text_color=GUI_CONSTANTS["TEXT_COLOR"],
                font=(GUI_CONSTANTS["FONT_FAMILY"], GUI_CONSTANTS["FONT_SIZE"]),
                height=50
            )
            self.text_widget.configure(state="disabled")
            
        except Exception as e:
            logger.error(f"Error creating chat bubble widgets: {e}")
            raise
            
    def _configure_grid(self):
        """Configure grid layout."""
        try:
            # Configure grid
            self.grid_columnconfigure(0, weight=1)
            
            # Place widgets
            self.text_widget.grid(
                row=0,
                column=0,
                sticky="nsew",
                padx=GUI_CONSTANTS["SMALL_PADDING"],
                pady=GUI_CONSTANTS["SMALL_PADDING"]
            )
            
        except Exception as e:
            logger.error(f"Error configuring chat bubble grid: {e}")
            raise
            
    def update_content(self, content: str):
        """Update bubble content."""
        try:
            if content != self.content:
                # Update content
                self.content = content
                
                # Update text widget
                self.text_widget.configure(state="normal")
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", content)
                self.text_widget.configure(state="disabled")
                
                # Update height
                self.text_widget.configure(height=min(200, max(50, len(content.split("\n")) * 20)))
                
        except Exception as e:
            logger.error(f"Error updating chat bubble content: {e}")
            raise
