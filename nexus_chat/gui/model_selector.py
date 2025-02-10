"""Model selector module."""
import asyncio
import logging
from typing import Callable, List, Optional

import customtkinter as ctk

from nexus_chat.backend.service import BackendService

logger = logging.getLogger(__name__)

class ModelSelector(ctk.CTkFrame):
    """Model selector widget."""
    
    def __init__(
        self,
        parent: ctk.CTk,
        backend: BackendService,
        on_model_loaded: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        """Initialize model selector.
        
        Args:
            parent: Parent widget
            backend: Backend service
            on_model_loaded: Callback for when model is loaded
            **kwargs: Additional arguments
        """
        try:
            logger.info("Initializing model selector")
            
            # Initialize parent
            super().__init__(parent, **kwargs)
            
            # Store references
            self.parent = parent
            self.backend = backend
            self.on_model_loaded = on_model_loaded
            
            # Initialize state
            self.models = []
            self.selected_model = None
            self.is_loading = False
            
            # Configure frame
            self.configure(
                fg_color="#2b2d30",
                corner_radius=6
            )
            
            # Create widgets
            self._create_widgets()
            
            # Load models
            self.after(100, self._load_models)
            
            logger.info("Model selector initialized")
            
        except Exception as e:
            logger.error(f"Error initializing model selector: {str(e)}")
            raise
            
    def _create_widgets(self):
        """Create model selector widgets."""
        try:
            logger.info("Creating model selector widgets")
            
            # Configure grid
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=0)
            
            # Create model dropdown
            self.model_dropdown = ctk.CTkOptionMenu(
                self,
                values=["Loading models..."],
                command=self._on_model_selected,
                width=200,
                font=("Segoe UI", 12),
                dropdown_font=("Segoe UI", 12),
                button_color="#404754",
                button_hover_color="#4a72f5",
                fg_color="#1e1f22",
                text_color="#ffffff",
                dropdown_text_color="#ffffff",
                dropdown_fg_color="#1e1f22",
                dropdown_hover_color="#404754"
            )
            self.model_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            # Create load button
            self.load_button = ctk.CTkButton(
                self,
                text="Load",
                command=self._on_load_clicked,
                width=100,
                font=("Segoe UI", 12, "bold"),
                fg_color="#4a72f5",
                hover_color="#2952d9",
                height=32
            )
            self.load_button.grid(row=0, column=1, padx=10, pady=10)
            
            # Disable widgets initially
            self.model_dropdown.configure(state="disabled")
            self.load_button.configure(state="disabled")
            
            logger.info("Model selector widgets created")
            
        except Exception as e:
            logger.error(f"Error creating model selector widgets: {str(e)}")
            raise
            
    def _load_models(self):
        """Load available models."""
        try:
            logger.info("Loading models")
            
            # Set loading state
            self.is_loading = True
            self.model_dropdown.configure(
                values=["Loading models..."],
                state="disabled"
            )
            self.load_button.configure(state="disabled")
            
            # Start loading task
            asyncio.run_coroutine_threadsafe(
                self._load_models_async(),
                self.parent.loop
            )
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            self._handle_load_error("Failed to load models")
            
    async def _load_models_async(self):
        """Load models asynchronously."""
        try:
            # Get models
            self.models = await self.backend.list_models()
            
            # Update UI in main thread
            self.after(0, self._update_models_ui)
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            # Update UI in main thread
            self.after(0, lambda: self._handle_load_error(str(e)))
            
    def _update_models_ui(self):
        """Update UI with loaded models."""
        try:
            if not self.models:
                self._handle_load_error("No models found")
                return
                
            # Update dropdown
            self.model_dropdown.configure(
                values=self.models,
                state="normal"
            )
            
            # Get current model
            current_model = self.backend.get_model()
            if current_model and current_model in self.models:
                # Set current model
                self.model_dropdown.set(current_model)
                self.selected_model = current_model
                self.load_button.configure(state="normal")
            elif self.models:
                # Set first model
                self.model_dropdown.set(self.models[0])
                self.selected_model = self.models[0]
                self.load_button.configure(state="normal")
                
            # Update state
            self.is_loading = False
            
            logger.info(f"Models loaded: {self.models}")
            
        except Exception as e:
            logger.error(f"Error updating models UI: {str(e)}")
            self._handle_load_error(str(e))
            
    def _handle_load_error(self, error_msg: str):
        """Handle model loading error.
        
        Args:
            error_msg: Error message
        """
        self.is_loading = False
        self.models = []
        self.selected_model = None
        
        self.model_dropdown.configure(
            values=[f"Error: {error_msg}"],
            state="disabled"
        )
        self.load_button.configure(state="disabled")
            
    def _on_model_selected(self, model: str):
        """Handle model selection.
        
        Args:
            model: Selected model
        """
        try:
            # Ignore if loading or error
            if self.is_loading or model.startswith("Error:") or model == "Loading models...":
                return
                
            logger.info(f"Model selected: {model}")
            
            # Store selected model
            self.selected_model = model
            
            # Enable load button
            self.load_button.configure(state="normal")
            
        except Exception as e:
            logger.error(f"Error handling model selection: {str(e)}")
            raise
            
    def _on_load_clicked(self):
        """Handle load button click."""
        try:
            logger.info("Load button clicked")
            
            # Check if model selected
            if not self.selected_model or self.is_loading:
                return
                
            # Disable widgets
            self.model_dropdown.configure(state="disabled")
            self.load_button.configure(state="disabled")
            
            try:
                # Set model
                self.backend.set_model(self.selected_model)
                
                # Call callback
                if self.on_model_loaded:
                    self.on_model_loaded(self.selected_model)
                    
                logger.info(f"Model loaded: {self.selected_model}")
                
            finally:
                # Re-enable widgets
                self.model_dropdown.configure(state="normal")
                self.load_button.configure(state="normal")
            
        except Exception as e:
            logger.error(f"Error handling load button click: {str(e)}")
            raise
