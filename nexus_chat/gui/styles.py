"""GUI styles and theme configuration."""
from typing import Dict, Any
import customtkinter as ctk

# Color schemes
THEMES = {
    "dark": {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2d2d2d",
        "fg_primary": "#ffffff",
        "fg_secondary": "#cccccc",
        "accent": "#007acc",
        "accent_hover": "#0098ff",
        "error": "#ff3333",
        "success": "#33cc33",
        "warning": "#ffcc00",
        "border": "#404040",
        "selection": "#264f78",
        "placeholder": "#808080"
    },
    "light": {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f0f0f0",
        "fg_primary": "#000000",
        "fg_secondary": "#666666",
        "accent": "#0078d4",
        "accent_hover": "#106ebe",
        "error": "#e81123",
        "success": "#107c10",
        "warning": "#ff8c00",
        "border": "#d1d1d1",
        "selection": "#cce8ff",
        "placeholder": "#767676"
    }
}

# Widget styles
STYLES = {
    "default": {
        "font": ("Segoe UI", 12),
        "heading_font": ("Segoe UI", 16, "bold"),
        "button_font": ("Segoe UI", 12),
        "code_font": ("Cascadia Code", 12),
        "padding": {"padx": 10, "pady": 5},
        "border_width": 1,
        "corner_radius": 6
    }
}

class ThemeManager:
    """Manages application theming and styles."""
    
    def __init__(self):
        """Initialize theme manager with default theme."""
        self.current_theme = "dark"
        self._apply_theme()

    def _apply_theme(self):
        """Apply current theme to customtkinter."""
        theme = THEMES[self.current_theme]
        
        # Configure customtkinter appearance
        ctk.set_appearance_mode("dark" if self.current_theme == "dark" else "light")
        
        # Configure default color theme
        ctk.set_default_color_theme("blue")
        
        # Configure widget colors
        self._configure_colors(theme)

    def _configure_colors(self, theme: Dict[str, str]):
        """Configure widget colors based on theme."""
        # Text colors
        ctk.ThemeManager.theme["CTkLabel"]["text_color"] = theme["fg_primary"]
        ctk.ThemeManager.theme["CTkEntry"]["text_color"] = theme["fg_primary"]
        ctk.ThemeManager.theme["CTkTextbox"]["text_color"] = theme["fg_primary"]
        
        # Background colors
        ctk.ThemeManager.theme["CTk"]["fg_color"] = theme["bg_primary"]
        ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = theme["bg_secondary"]
        ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = theme["bg_secondary"]
        ctk.ThemeManager.theme["CTkTextbox"]["fg_color"] = theme["bg_secondary"]
        
        # Button colors
        ctk.ThemeManager.theme["CTkButton"]["fg_color"] = theme["accent"]
        ctk.ThemeManager.theme["CTkButton"]["hover_color"] = theme["accent_hover"]
        ctk.ThemeManager.theme["CTkButton"]["text_color"] = theme["fg_primary"]
        
        # Border colors
        ctk.ThemeManager.theme["CTkEntry"]["border_color"] = theme["border"]
        ctk.ThemeManager.theme["CTkTextbox"]["border_color"] = theme["border"]

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def get_style(self, widget_type: str) -> Dict[str, Any]:
        """Get style configuration for a widget type."""
        base_style = STYLES["default"].copy()
        
        # Add theme-specific colors
        theme = THEMES[self.current_theme]
        if widget_type == "button":
            base_style.update({
                "fg_color": theme["accent"],
                "hover_color": theme["accent_hover"],
                "text_color": theme["fg_primary"],
                "font": STYLES["default"]["button_font"]
            })
        elif widget_type == "entry":
            base_style.update({
                "fg_color": theme["bg_secondary"],
                "text_color": theme["fg_primary"],
                "placeholder_text_color": theme["placeholder"],
                "border_color": theme["border"]
            })
        elif widget_type == "textbox":
            base_style.update({
                "fg_color": theme["bg_secondary"],
                "text_color": theme["fg_primary"],
                "border_color": theme["border"]
            })
        elif widget_type == "frame":
            base_style.update({
                "fg_color": theme["bg_secondary"]
            })
        elif widget_type == "heading":
            base_style.update({
                "text_color": theme["fg_primary"],
                "font": STYLES["default"]["heading_font"]
            })
        
        return base_style

# Global theme manager instance
theme_manager = ThemeManager()
