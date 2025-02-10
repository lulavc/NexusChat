"""Model settings dialog module."""
import logging
import tkinter as tk
import customtkinter as ctk

from nexus_chat.utils.constants import GUI_CONSTANTS

logger = logging.getLogger(__name__)

class ModelSettingsDialog(ctk.CTkToplevel):
    """Model settings dialog."""
    
    def __init__(self, parent, chat_manager):
        """Initialize dialog."""
        super().__init__(parent)
        self.chat_manager = chat_manager
        self._setup_ui()
        logger.info("Initialized model settings dialog")

    def _setup_ui(self):
        """Setup UI components."""
        self.title("Model Settings")
        self.geometry("400x300")
        self.resizable(False, False)

        # Model selection
        self.model_label = ctk.CTkLabel(self, text="Select Model:")
        self.model_label.pack(pady=10)

        self.model_combobox = ctk.CTkComboBox(self)
        self.model_combobox.pack(pady=5)

        # Configuration controls
        self.temp_frame = ctk.CTkFrame(self)
        self.temp_frame.pack(pady=10)

        self.temp_label = ctk.CTkLabel(self.temp_frame, text="Temperature:")
        self.temp_label.grid(row=0, column=0)

        self.temp_slider = ctk.CTkSlider(self.temp_frame, from_=0, to=1)
        self.temp_slider.grid(row=0, column=1)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        self.save_button = ctk.CTkButton(self.button_frame, text="Save", command=self._save)
        self.save_button.grid(row=0, column=0, padx=5)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=5)

    def _save(self):
        """Save settings."""
        try:
            # Save model settings
            self.chat_manager.update_model_settings(
                model=self.model_combobox.get(),
                temperature=self.temp_slider.get()
            )
            self.destroy()
            logger.info("Model settings saved")
        except Exception as e:
            logger.error(f"Error saving model settings: {e}")
            self.master.show_error(f"Error saving model settings: {str(e)}")

    def show(self):
        """Show dialog."""
        self.grab_set()
        self.wait_window()
