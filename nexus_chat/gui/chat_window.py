"""Chat window module with enhanced styling and features."""
import asyncio
import logging
import re
from typing import Optional

import customtkinter as ctk

from nexus_chat.backend.service import BackendService
from nexus_chat.models.message import Message, MessageRole
from nexus_chat.utils.constants import CHAT_WINDOW_DEFAULTS

logger = logging.getLogger(__name__)

class EnhancedTextBox(ctk.CTkTextbox):
    """Enhanced text box with syntax highlighting and custom styling."""
    
    def __init__(self, *args, **kwargs):
        """Initialize enhanced text box."""
        super().__init__(*args, **kwargs)
        
        # Configure tags for different message types
        self.tag_configure("user_message", 
            background="#2b2d30",
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=10,
            spacing2=5,
            spacing3=10
        )
        
        self.tag_configure("assistant_message",
            background="#1e1f22",
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=10,
            spacing2=5,
            spacing3=10
        )
        
        self.tag_configure("role_label",
            foreground="#8a8f99",
            font=("Segoe UI", 11, "bold"),
            spacing1=5,
            spacing2=5
        )
        
        self.tag_configure("code_block",
            background="#000000",
            font=("Cascadia Code", 11),
            lmargin1=40,
            lmargin2=40,
            rmargin=20,
            spacing1=10,
            spacing2=10,
            spacing3=10
        )
        
        # Configure syntax highlighting tags
        self.tag_configure("keyword", foreground="#ff79c6", font=("Cascadia Code", 11))
        self.tag_configure("string", foreground="#f1fa8c", font=("Cascadia Code", 11))
        self.tag_configure("comment", foreground="#6272a4", font=("Cascadia Code", 11))
        self.tag_configure("number", foreground="#bd93f9", font=("Cascadia Code", 11))
        self.tag_configure("function", foreground="#50fa7b", font=("Cascadia Code", 11))
        
        # Configure selection colors
        self.configure(
            selectbackground="#404754",
            selectforeground="#ffffff"
        )
        
    def highlight_code(self, code: str, language: str) -> str:
        """Apply syntax highlighting to code.
        
        Args:
            code: Code to highlight
            language: Programming language
            
        Returns:
            Highlighted code
        """
        try:
            # Define regex patterns for syntax elements
            patterns = {
                'keyword': r'\b(def|class|import|from|return|if|else|elif|for|while|try|except|with|as|in|is|not|and|or)\b',
                'string': r'\".*?\"|\'.*?\'',
                'comment': r'#[^\n]*',
                'number': r'\b\d+\b',
                'function': r'\b\w+(?=\s*\()',
            }
            
            # Get current position
            current_pos = self.index("insert")
            
            # Insert code with base tag
            self.insert("insert", code, "code_block")
            
            # Apply syntax highlighting
            start_pos = self.index("insert linestart")
            for line in code.split('\n'):
                for tag, pattern in patterns.items():
                    for match in re.finditer(pattern, line):
                        start, end = match.span()
                        # Calculate absolute positions
                        abs_start = f"{start_pos}+{start}c"
                        abs_end = f"{start_pos}+{end}c"
                        self.tag_add(tag, abs_start, abs_end)
                start_pos = self.index(f"{start_pos}+1line")
                
        except Exception as e:
            logger.error(f"Error highlighting code: {str(e)}")
            # Fall back to plain text
            self.insert("insert", code)

class ChatWindow(ctk.CTkFrame):
    """Enhanced chat window widget."""
    
    def __init__(
        self,
        parent: ctk.CTk,
        backend: BackendService,
        **kwargs
    ):
        """Initialize chat window.
        
        Args:
            parent: Parent widget
            backend: Backend service
            **kwargs: Additional arguments
        """
        try:
            logger.info("Initializing chat window")
            
            # Initialize parent
            super().__init__(parent, **kwargs)
            
            # Store references
            self.parent = parent
            self.backend = backend
            
            # Initialize state
            self.is_sending = False
            self.message_queue = []
            self.current_response = ""
            
            # Create widgets
            self._create_widgets()
            
            # Setup bindings
            self._setup_bindings()
            
            # Start processing messages
            self.after(100, self._process_messages)
            
            logger.info("Chat window initialized")
            
        except Exception as e:
            logger.error(f"Error initializing chat window: {str(e)}")
            raise
            
    def _create_widgets(self):
        """Create chat window widgets."""
        try:
            logger.info("Creating chat window widgets")
            
            # Configure grid
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)
            self.grid_columnconfigure(0, weight=1)
            
            # Create chat display
            self.chat_display = EnhancedTextBox(
                self,
                height=400,
                font=("Segoe UI", 12),
                text_color="#ffffff",
                fg_color="#1e1f22",
                border_width=0,
                activate_scrollbars=True
            )
            self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            # Create input frame
            self.input_frame = ctk.CTkFrame(
                self,
                fg_color="#2b2d30",
                border_width=1,
                border_color="#3d3f41"
            )
            self.input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            # Configure input frame grid
            self.input_frame.grid_columnconfigure(0, weight=1)
            self.input_frame.grid_columnconfigure(1, weight=0)
            
            # Create message input
            self.message_input = ctk.CTkTextbox(
                self.input_frame,
                height=CHAT_WINDOW_DEFAULTS["INPUT_HEIGHT"],
                font=("Segoe UI", 12),
                fg_color="#1e1f22",
                border_width=0,
                wrap="word"
            )
            self.message_input.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
            
            # Create send button
            self.send_button = ctk.CTkButton(
                self.input_frame,
                text="Send",
                font=("Segoe UI", 12, "bold"),
                command=self._send_message,
                fg_color="#4a72f5",
                hover_color="#2952d9",
                height=35
            )
            self.send_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)
            
            logger.info("Chat window widgets created")
            
        except Exception as e:
            logger.error(f"Error creating chat window widgets: {str(e)}")
            raise
            
    def _setup_bindings(self):
        """Setup chat window bindings."""
        try:
            logger.info("Setting up chat window bindings")
            
            # Bind return key to send message
            self.message_input.bind("<Return>", self._handle_return)
            self.message_input.bind("<Shift-Return>", self._handle_shift_return)
            
            logger.info("Chat window bindings setup")
            
        except Exception as e:
            logger.error(f"Error setting up chat window bindings: {str(e)}")
            raise
            
    def _handle_return(self, event):
        """Handle return key press."""
        try:
            # Send message if not shift pressed
            self._send_message()
            
            # Prevent default
            return "break"
            
        except Exception as e:
            logger.error(f"Error handling return key press: {str(e)}")
            raise
            
    def _handle_shift_return(self, event):
        """Handle shift+return key press."""
        try:
            # Insert newline
            self.message_input.insert("insert", "\n")
            
            # Prevent default
            return "break"
            
        except Exception as e:
            logger.error(f"Error handling shift+return key press: {str(e)}")
            raise
            
    def _send_message(self):
        """Send message."""
        try:
            # Check if already sending
            if self.is_sending:
                return
                
            # Get message
            message = self.message_input.get("1.0", "end-1c").strip()
            
            # Check message
            if not message:
                return
                
            # Clear input
            self.message_input.delete("1.0", "end")
            
            # Add message to queue
            self.message_queue.append(message)
            
            # Update state
            self.is_sending = True
            
            # Update UI
            self._update_ui_state()
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
            
    def _update_ui_state(self):
        """Update UI state."""
        try:
            # Update input state
            self.message_input.configure(state="disabled" if self.is_sending else "normal")
            self.send_button.configure(state="disabled" if self.is_sending else "normal")
            
        except Exception as e:
            logger.error(f"Error updating UI state: {str(e)}")
            raise
            
    def _display_message(self, message: Message):
        """Display message.
        
        Args:
            message: Message to display
        """
        try:
            # Enable editing
            self.chat_display.configure(state="normal")
            
            # Add newline if not empty
            if self.chat_display.get("1.0", "end-1c"):
                self.chat_display.insert("end", "\n\n")
            
            # Get message tag
            tag = "user_message" if message.role == MessageRole.USER else "assistant_message"
            
            # Add role label
            role_text = "You" if message.role == MessageRole.USER else "Assistant"
            self.chat_display.insert("end", f"{role_text}\n", ("role_label", tag))
            
            # Process content
            content = message.content.strip()
            
            # Find code blocks
            parts = re.split(r'(```\w+\n.*?\n```)', content, flags=re.DOTALL)
            
            for part in parts:
                if part.startswith('```') and part.endswith('```'):
                    # Extract language and code
                    match = re.match(r'```(\w+)\n(.*?)\n```', part, re.DOTALL)
                    if match:
                        lang, code = match.groups()
                        self.chat_display.highlight_code(code.strip(), lang)
                        self.chat_display.insert("end", "\n")
                else:
                    # Add regular text
                    if part.strip():
                        self.chat_display.insert("end", part.strip() + "\n", tag)
            
            # Scroll to bottom
            self.chat_display.see("end")
            
            # Disable editing
            self.chat_display.configure(state="disabled")
            
        except Exception as e:
            logger.error(f"Error displaying message: {str(e)}")
            raise
            
    def _update_streaming_response(self, chunk: str):
        """Update streaming response.
        
        Args:
            chunk: Response chunk
        """
        try:
            # Enable editing
            self.chat_display.configure(state="normal")
            
            # Update response
            if not self.current_response:
                # First chunk, add assistant prefix
                if self.chat_display.get("1.0", "end-1c"):
                    self.chat_display.insert("end", "\n\n")
                self.chat_display.insert("end", "Assistant\n", ("role_label", "assistant_message"))
                
            # Add chunk
            self.current_response += chunk
            
            # Find last message
            last_pos = self.chat_display.index("end-1c linestart")
            self.chat_display.delete(f"{last_pos} linestart", "end-1c")
            
            # Process content
            parts = re.split(r'(```\w+\n.*?\n```)', self.current_response, flags=re.DOTALL)
            
            for part in parts:
                if part.startswith('```') and part.endswith('```'):
                    # Extract language and code
                    match = re.match(r'```(\w+)\n(.*?)\n```', part, re.DOTALL)
                    if match:
                        lang, code = match.groups()
                        self.chat_display.highlight_code(code.strip(), lang)
                        self.chat_display.insert("end", "\n")
                else:
                    # Add regular text
                    if part.strip():
                        self.chat_display.insert("end", part.strip() + "\n", "assistant_message")
            
            # Scroll to bottom
            self.chat_display.see("end")
            
            # Disable editing
            self.chat_display.configure(state="disabled")
            
        except Exception as e:
            logger.error(f"Error updating streaming response: {str(e)}")
            raise
            
    def _process_messages(self):
        """Process messages from queue."""
        try:
            # Check if there are messages to process
            if self.message_queue and not self.is_sending:
                # Get message
                message = self.message_queue.pop(0)
                
                # Create user message
                user_message = Message(
                    role=MessageRole.USER,
                    content=message
                )
                
                # Display user message
                self._display_message(user_message)
                
                # Reset current response
                self.current_response = ""
                
                # Send message
                asyncio.run_coroutine_threadsafe(
                    self.backend.send_message(message, self._update_streaming_response),
                    self.parent.loop
                )
                
            # Schedule next check
            self.after(100, self._process_messages)
            
        except Exception as e:
            logger.error(f"Error processing messages: {str(e)}")
            # Show error to user
            error_message = Message(
                role=MessageRole.SYSTEM,
                content=f"Error: {str(e)}"
            )
            self._display_message(error_message)
            
            # Update state
            self.is_sending = False
            self._update_ui_state()
