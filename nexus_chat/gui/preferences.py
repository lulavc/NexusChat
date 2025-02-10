"""Preferences dialog module."""
import logging
import customtkinter as ctk

logger = logging.getLogger(__name__)

class PreferencesDialog(ctk.CTkToplevel):
    """Preferences dialog."""
    
    def __init__(self, parent, chat_manager):
        super().__init__(parent)
        self.chat_manager = chat_manager
        self._setup_ui()
        logger.info("Preferences dialog initialized")

    def _setup_ui(self):
        self.title("Application Preferences")
        self.geometry("400x300")
        
        # Add preference controls here
        tab = ctk.CTkTabview(self)
        tab.pack(fill='both', expand=True)
        appearance_tab = tab.add("Appearance")
        self._create_appearance_tab(appearance_tab)
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.ok_button.pack(pady=20)

    def _create_appearance_tab(self, tab):
        # Theme selection
        self.theme_var = ctk.StringVar(value=ThemeManager.load_theme()['mode'].title())
        ctk.CTkLabel(tab, text='Appearance Mode:').pack(anchor='w')
        ctk.CTkOptionMenu(
            tab,
            variable=self.theme_var,
            values=['Dark', 'Light', 'System']
        ).pack(fill='x', pady=(0, 15))

        # Color theme
        self.color_theme_var = ctk.StringVar(value=ThemeManager.load_theme()['color_theme'])
        ctk.CTkLabel(tab, text='Color Theme:').pack(anchor='w')
        ctk.CTkOptionMenu(
            tab,
            variable=self.color_theme_var,
            values=['blue', 'green', 'dark-blue', 'high-contrast']
        ).pack(fill='x')

    def show(self):
        """Show dialog."""
        self.grab_set()
        self.wait_window()
