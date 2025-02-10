import customtkinter as ctk
from ..utils.theme_manager import ThemeManager

class AccessibleMixin:
    def init_accessibility(self):
        self.bind('<Control-Shift-A>', self.toggle_accessibility)
        self.high_contrast = False
        self._apply_theme_settings()

    def toggle_accessibility(self, event=None):
        self.high_contrast = not self.high_contrast
        self._apply_theme_settings()

    def _apply_theme_settings(self):
        if self.high_contrast:
            ctk.set_appearance_mode('dark')
            ctk.set_default_color_theme('high-contrast')
        else:
            theme_config = ThemeManager.load_theme()
            ctk.set_appearance_mode(theme_config['mode'])
            ctk.set_default_color_theme(theme_config['color_theme'])
