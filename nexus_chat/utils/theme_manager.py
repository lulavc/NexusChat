"""Theme manager module."""
import logging

import customtkinter as ctk

from nexus_chat.utils.constants import GUI_CONSTANTS

logger = logging.getLogger(__name__)

class ThemeManager:
    """Theme manager."""
    
    def __init__(self):
        """Initialize theme manager."""
        try:
            logger.info("Initializing theme manager")
            
            # Set appearance mode
            ctk.set_appearance_mode("dark")
            
            # Set default color theme
            ctk.set_default_color_theme("dark-blue")
            
            logger.info("Theme manager initialized")
            
        except Exception as e:
            logger.error(f"Error initializing theme manager: {str(e)}")
            raise
