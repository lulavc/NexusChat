"""Ollama API client module."""
import aiohttp
import json
import logging
import requests
from typing import AsyncGenerator, Dict, List, Optional, Generator

logger = logging.getLogger(__name__)

class OllamaClient:
    """Ollama API client."""
    
    def __init__(self, host: str = "http://localhost:11434"):
        """Initialize client."""
        try:
            self.host = host
            self.session: Optional[aiohttp.ClientSession] = None
            self.base_url = host.rstrip('/')
            logger.info(f"Initialized Ollama client with base URL: {host}")
        except Exception as e:
            logger.error(f"Error initializing Ollama client: {str(e)}")
            raise
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists."""
        try:
            if not self.session or self.session.closed:
                self.session = aiohttp.ClientSession()
                logger.debug("Created new aiohttp session")
        except Exception as e:
            logger.error(f"Error ensuring session: {str(e)}")
            raise
    
    async def close(self):
        """Close client session."""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
                self.session = None
                logger.debug("Closed aiohttp session")
        except Exception as e:
            logger.error(f"Error closing session: {str(e)}")
            raise
    
    async def generate(
        self,
        prompt: str,
        model: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        options: Optional[Dict] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate response from Ollama model.
        
        Args:
            prompt: The prompt to send to the model
            model: Name of the model to use
            system: Optional system prompt
            template: Optional prompt template
            context: Optional context window
            options: Optional model parameters
        """
        await self._ensure_session()
        
        # Prepare request data
        data = {
            "model": model,
            "prompt": prompt,
            "stream": True,
        }
        
        if system:
            data["system"] = system
        if template:
            data["template"] = template
        if context:
            data["context"] = context
        if options:
            data["options"] = options
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "error" in chunk:
                                logger.error(f"Ollama API error: {chunk['error']}")
                                raise RuntimeError(chunk["error"])
                            if "response" in chunk:
                                yield chunk["response"]
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding response: {e}")
                            continue
                            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def list_models(self) -> List[str]:
        """Get list of available models."""
        await self._ensure_session()
        
        try:
            logger.info("Listing available models")
            
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                response.raise_for_status()
                data = await response.json()
                models = [model["name"] for model in data["models"]]
                
                logger.info(f"Found {len(models)} models: {models}")
                return models
                
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            raise
            
    async def chat(
        self,
        model: str,
        message: str,
    ) -> AsyncGenerator[str, None]:
        """Send chat message to model with streaming response.
        
        Args:
            model: Name of model to use
            message: Message to send
            
        Yields:
            Response chunks from the model
        """
        await self._ensure_session()
        
        try:
            # Log request
            logger.info(f"Sending message to {model}")
            
            # Format message
            messages = [{"role": "user", "content": message}]
            
            # Send request
            async with self.session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                }
            ) as response:
                # Check response
                response.raise_for_status()
                
                # Initialize chunk buffer for better formatting
                chunk_buffer = ""
                code_block = False
                
                # Read response chunks
                async for line in response.content:
                    # Skip empty lines
                    if not line:
                        continue
                        
                    # Parse response
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse response line: {line}")
                        continue
                        
                    # Check error
                    if "error" in data:
                        raise Exception(data["error"])
                        
                    # Extract and format response chunk
                    if "message" in data and "content" in data["message"]:
                        chunk = data["message"]["content"]
                        
                        # Handle code block formatting
                        if "```" in chunk:
                            code_block = not code_block
                            if code_block:
                                # Start of code block
                                chunk_buffer += "\n" + chunk
                            else:
                                # End of code block
                                chunk_buffer += chunk + "\n"
                        else:
                            if code_block:
                                # Inside code block - preserve formatting
                                chunk_buffer += chunk
                            else:
                                # Outside code block - format for readability
                                if chunk.strip() in [".", "!", "?"] and chunk_buffer:
                                    chunk_buffer += chunk + "\n"
                                else:
                                    chunk_buffer += chunk
                        
                        # Yield formatted chunk
                        if chunk_buffer:
                            if "\n" in chunk_buffer or len(chunk_buffer) > 80:
                                yield chunk_buffer
                                chunk_buffer = ""
                
                # Yield any remaining content
                if chunk_buffer:
                    yield chunk_buffer
                    
                logger.info("Message sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
            
    async def chat_stream(
        self,
        model: str,
        message: str,
        context: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses from model.
        
        Args:
            model: Name of model to use
            message: Message to send
            context: Optional chat context from previous messages
            **kwargs: Additional parameters for the model
            
        Yields:
            Chunks of the model's response
        """
        await self._ensure_session()
        
        try:
            # Prepare request
            data = {
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "stream": True,
                **kwargs
            }
            
            if context:
                data["messages"] = context + data["messages"]
                
            # Send request
            async with self.session.post(
                f"{self.base_url}/api/chat",
                json=data
            ) as response:
                # Check response
                response.raise_for_status()
                
                # Stream response
                async for line in response.content:
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                yield chunk["message"]["content"]
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding response: {e}")
                            continue
                        
        except Exception as e:
            logger.error(f"Error streaming chat: {str(e)}")
            raise
            
    async def pull_model(self, model: str):
        """Pull model."""
        await self._ensure_session()
        
        try:
            logger.info(f"Pulling model {model}")
            
            async with self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model}
            ) as response:
                response.raise_for_status()
                
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if "error" in data:
                                raise Exception(data["error"])
                            if "status" in data:
                                logger.info(f"Pull status: {data['status']}")
                        except json.JSONDecodeError:
                            continue
                            
                logger.info(f"Model {model} pulled successfully")
                
        except Exception as e:
            logger.error(f"Error pulling model: {str(e)}")
            raise
