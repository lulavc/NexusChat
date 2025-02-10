"""API configuration dialog module."""
import logging
import tkinter as tk
import customtkinter as ctk

from nexus_chat.utils.constants import GUI_CONSTANTS

logger = logging.getLogger(__name__)

class APIConfigDialog(ctk.CTkToplevel):
    """API configuration dialog."""
    
    def __init__(self, parent, chat_manager):
        """Initialize dialog."""
        super().__init__(parent)
        self.chat_manager = chat_manager
        self._setup_ui()
        logger.info("Initialized API config dialog")

    def _setup_ui(self):
        """Setup UI components."""
        self.title("API Configuration")
        self.geometry("400x300")
        self.resizable(False, False)

        # API endpoint
        self.endpoint_frame = ctk.CTkFrame(self)
        self.endpoint_frame.pack(pady=10)

        self.endpoint_label = ctk.CTkLabel(self.endpoint_frame, text="API Endpoint:")
        self.endpoint_label.grid(row=0, column=0)

        self.endpoint_entry = ctk.CTkEntry(self.endpoint_frame)
        self.endpoint_entry.grid(row=0, column=1)

        # API key
        self.key_frame = ctk.CTkFrame(self)
        self.key_frame.pack(pady=10)

        self.key_label = ctk.CTkLabel(self.key_frame, text="API Key:")
        self.key_label.grid(row=0, column=0)

        self.key_entry = ctk.CTkEntry(self.key_frame, show="*")
        self.key_entry.grid(row=0, column=1)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        self.test_button = ctk.CTkButton(self.button_frame, text="Test Connection", command=self._test_connection)
        self.test_button.grid(row=0, column=0, padx=5)

        self.save_button = ctk.CTkButton(self.button_frame, text="Save", command=self._save)
        self.save_button.grid(row=0, column=1, padx=5)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=0, column=2, padx=5)

    def _test_connection(self):
        """Test API connection."""
        try:
            self.chat_manager.test_api_connection(
                endpoint=self.endpoint_entry.get(),
                api_key=self.key_entry.get()
            )
            logger.info("API connection test successful")
            self.master.show_info("API connection successful!")
        except Exception as e:
            logger.error(f"Error testing API connection: {e}")
            self.master.show_error(f"Error testing API connection: {str(e)}")

    def _save(self):
        """Save API configuration."""
        try:
            self.chat_manager.update_api_config(
                endpoint=self.endpoint_entry.get(),
                api_key=self.key_entry.get()
            )
            self.destroy()
            logger.info("API configuration saved")
        except Exception as e:
            logger.error(f"Error saving API configuration: {e}")
            self.master.show_error(f"Error saving API configuration: {str(e)}")

    def show(self):
        """Show dialog."""
        self.grab_set()
        self.wait_window()
