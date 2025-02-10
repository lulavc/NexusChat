"""Settings panel component."""
import customtkinter as ctk
from typing import Callable, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SettingsPanel(ctk.CTkToplevel):
    """Settings panel window."""
    
    def __init__(
        self,
        parent,
        settings: Dict[str, Any],
        on_save: Callable[[Dict[str, Any]], None]
    ):
        """Initialize settings panel."""
        super().__init__(parent)
        
        self.settings = settings.copy()
        self.on_save = on_save
        
        # Configure window
        self.title("Settings")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Hide initially
        self.withdraw()
        
        # Initialize components
        self._init_components()
    
    def _init_components(self):
        """Initialize panel components."""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Settings",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 20))
        
        # API Settings
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", pady=(0, 20))
        
        api_label = ctk.CTkLabel(
            api_frame,
            text="API Settings",
            font=("Arial", 16, "bold")
        )
        api_label.pack(pady=(10, 5))
        
        # API Host
        host_label = ctk.CTkLabel(api_frame, text="Ollama Host:")
        host_label.pack(pady=(5, 0))
        
        self.host_entry = ctk.CTkEntry(api_frame)
        self.host_entry.pack(fill="x", padx=20)
        self.host_entry.insert(0, self.settings.get("ollama_host", "http://localhost:11434"))
        
        # Model Settings
        model_frame = ctk.CTkFrame(main_frame)
        model_frame.pack(fill="x", pady=(0, 20))
        
        model_label = ctk.CTkLabel(
            model_frame,
            text="Model Settings",
            font=("Arial", 16, "bold")
        )
        model_label.pack(pady=(10, 5))
        
        # Default Model
        default_model_label = ctk.CTkLabel(model_frame, text="Default Model:")
        default_model_label.pack(pady=(5, 0))
        
        self.model_entry = ctk.CTkEntry(model_frame)
        self.model_entry.pack(fill="x", padx=20)
        self.model_entry.insert(0, self.settings.get("default_model", "mistral"))
        
        # System Prompt
        system_prompt_label = ctk.CTkLabel(model_frame, text="System Prompt:")
        system_prompt_label.pack(pady=(10, 0))
        
        self.system_prompt_text = ctk.CTkTextbox(
            model_frame,
            height=100
        )
        self.system_prompt_text.pack(fill="x", padx=20)
        self.system_prompt_text.insert(
            "1.0",
            self.settings.get("system_prompt", "You are a helpful AI assistant.")
        )
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self._on_save
        )
        save_button.pack(side="left", padx=5)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.hide
        )
        cancel_button.pack(side="right", padx=5)
    
    def _on_save(self):
        """Handle save button click."""
        try:
            # Update settings
            self.settings["ollama_host"] = self.host_entry.get().strip()
            self.settings["default_model"] = self.model_entry.get().strip()
            self.settings["system_prompt"] = self.system_prompt_text.get("1.0", "end-1c").strip()
            
            # Call save callback
            self.on_save(self.settings)
            
            # Hide panel
            self.hide()
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            # Show error message
    
    def show(self):
        """Show the settings panel."""
        self.deiconify()
    
    def hide(self):
        """Hide the settings panel."""
        self.withdraw()
