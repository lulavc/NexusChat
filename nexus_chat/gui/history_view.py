"""Chat history view component."""
import customtkinter as ctk
from typing import Callable, List, Optional
import logging
from datetime import datetime

from nexus_chat.models.chat_session import ChatSession
from nexus_chat.utils.constants import GUI_CONSTANTS

logger = logging.getLogger(__name__)

class HistoryView(ctk.CTkScrollableFrame):
    """View for displaying chat history."""
    
    def __init__(self, master, command: Optional[Callable[[str], None]] = None):
        """Initialize history view."""
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=0
        )
        
        self.command = command
        self.sessions: List[ChatSession] = []
        self.session_frames = {}
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Create header
        header = ctk.CTkLabel(
            self,
            text="Chat History",
            font=(
                GUI_CONSTANTS["DEFAULT_FONT"],
                GUI_CONSTANTS["HEADING_FONT_SIZE"],
                "bold"
            )
        )
        header.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 10))
    
    def _format_timestamp(self, timestamp: datetime) -> str:
        """Format timestamp for display."""
        now = datetime.now()
        delta = now - timestamp
        
        if delta.days == 0:
            if delta.seconds < 60:
                return "Just now"
            elif delta.seconds < 3600:
                minutes = delta.seconds // 60
                return f"{minutes}m ago"
            else:
                hours = delta.seconds // 3600
                return f"{hours}h ago"
        elif delta.days == 1:
            return "Yesterday"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        else:
            return timestamp.strftime("%Y-%m-%d")
    
    def _create_session_frame(self, session: ChatSession) -> ctk.CTkFrame:
        """Create a frame for a chat session."""
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)
        
        # Session name and timestamp
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        header_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=session.name,
            font=(GUI_CONSTANTS["DEFAULT_FONT"], GUI_CONSTANTS["DEFAULT_FONT_SIZE"])
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        time_label = ctk.CTkLabel(
            header_frame,
            text=self._format_timestamp(session.created_at),
            font=(GUI_CONSTANTS["DEFAULT_FONT"], GUI_CONSTANTS["DEFAULT_FONT_SIZE"]-2),
            text_color="gray"
        )
        time_label.grid(row=0, column=1, sticky="e")
        
        # Model name
        model_label = ctk.CTkLabel(
            frame,
            text=f"Model: {session.model}",
            font=(GUI_CONSTANTS["DEFAULT_FONT"], GUI_CONSTANTS["DEFAULT_FONT_SIZE"]-2),
            text_color="gray"
        )
        model_label.grid(row=1, column=0, sticky="w", padx=5, pady=(0, 2))
        
        # Message count
        msg_count = len(session.messages)
        msg_label = ctk.CTkLabel(
            frame,
            text=f"{msg_count} message{'s' if msg_count != 1 else ''}",
            font=(GUI_CONSTANTS["DEFAULT_FONT"], GUI_CONSTANTS["DEFAULT_FONT_SIZE"]-2),
            text_color="gray"
        )
        msg_label.grid(row=2, column=0, sticky="w", padx=5, pady=(0, 5))
        
        # Make entire frame clickable
        for widget in [frame, header_frame, name_label, time_label, model_label, msg_label]:
            widget.bind("<Button-1>", lambda e, s=session: self._on_session_click(s))
            widget.bind("<Enter>", lambda e, f=frame: self._on_frame_enter(f))
            widget.bind("<Leave>", lambda e, f=frame: self._on_frame_leave(f))
        
        return frame
    
    def _on_frame_enter(self, frame: ctk.CTkFrame):
        """Handle mouse enter on session frame."""
        frame.configure(fg_color=GUI_CONSTANTS["ACCENT_COLOR"])
    
    def _on_frame_leave(self, frame: ctk.CTkFrame):
        """Handle mouse leave on session frame."""
        frame.configure(fg_color=("gray90", "gray13"))
    
    def _on_session_click(self, session: ChatSession):
        """Handle session click."""
        if self.command:
            self.command(session.id)
    
    def update_sessions(self, sessions: List[ChatSession]):
        """Update the displayed sessions."""
        # Clear existing frames
        for frame in self.session_frames.values():
            frame.destroy()
        self.session_frames.clear()
        
        # Store sessions
        self.sessions = sessions
        
        # Create new frames
        for i, session in enumerate(sessions, start=1):
            frame = self._create_session_frame(session)
            frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            self.session_frames[session.id] = frame
    
    def get_selected_session(self) -> Optional[ChatSession]:
        """Get the currently selected session."""
        # Implement session selection if needed
        return None
