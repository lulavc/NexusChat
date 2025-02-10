"""Settings data model."""
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from pathlib import Path
import json

@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    size: float  # in GB
    strengths: List[str]
    capabilities: List[str]
    category: str
    default_system_prompt: str = "You are a helpful AI assistant."
    parameters: Dict[str, any] = field(default_factory=lambda: {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "max_tokens": 2048
    })

@dataclass
class AppSettings:
    """Application settings model."""
    
    # API Settings
    api_host: str = "http://localhost:11434"
    timeout: int = 30
    
    # UI Settings
    theme: str = "dark"
    font_size: int = 12
    font_family: str = "Segoe UI"
    window_width: int = 1200
    window_height: int = 800
    
    # Chat Settings
    default_model: str = "llama2"
    system_prompts: Dict[str, str] = field(default_factory=lambda: {
        "default": "You are a helpful AI assistant.",
        "code": "You are a helpful programming assistant.",
        "creative": "You are a creative writing assistant.",
        "academic": "You are a knowledgeable academic assistant."
    })
    max_history: int = 100
    stream_responses: bool = True
    
    # Storage Settings
    data_dir: Path = field(default_factory=lambda: Path.home() / ".config" / "ollama-chat")
    db_path: Optional[Path] = None
    auto_save: bool = True
    backup_enabled: bool = True
    backup_interval: int = 24  # hours
    
    # Logging Settings
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    console_logging: bool = True
    
    # Model Settings
    model_configs: Dict[str, ModelConfig] = field(default_factory=lambda: {
        "llama2": ModelConfig(
            name="LLaMA 2",
            size=6.7,  # 6.7B parameters
            category="Science and Analysis",
            strengths=[
                "Explicações científicas detalhadas",
                "Problemas de física",
                "Conceitos científicos",
                "Demonstrações passo a passo"
            ],
            capabilities=[
                "Física e ciências naturais",
                "Explicações conceituais",
                "Análise de problemas complexos",
                "Demonstrações matemáticas"
            ],
            parameters={
                "temperature": 0.5,
                "top_p": 0.9,
                "context_length": 4096,
                "embedding_length": 4096,
                "architecture": "llama",
                "quantization": "Q4_0"
            },
            default_system_prompt="You are a scientific assistant specialized in physics and natural sciences."
        ),
        "mistral": ModelConfig(
            name="Mistral",
            size=7.2,  # 7.2B parameters
            category="Mathematics",
            strengths=[
                "Resolução precisa de equações",
                "Álgebra e cálculos matemáticos",
                "Explicações passo a passo",
                "Fórmulas matemáticas"
            ],
            capabilities=[
                "Equações de primeiro e segundo grau",
                "Álgebra linear",
                "Cálculo diferencial e integral",
                "Geometria analítica"
            ],
            parameters={
                "temperature": 0.2,
                "top_p": 0.9,
                "context_length": 32768,
                "embedding_length": 4096,
                "architecture": "llama",
                "quantization": "Q4_0"
            },
            default_system_prompt="You are a precise mathematical assistant, specialized in solving equations and mathematical problems step by step."
        ),
        "codellama": ModelConfig(
            name="CodeLlama",
            size=6.7,  # 6.7B parameters
            category="Programming",
            strengths=[
                "Geração de código",
                "Debugging",
                "Documentação técnica",
                "Análise de código"
            ],
            capabilities=[
                "Programação em múltiplas linguagens",
                "Refatoração de código",
                "Sugestões de melhores práticas",
                "Otimização de código"
            ],
            parameters={
                "temperature": 0.5,
                "top_p": 0.9,
                "context_length": 16384,
                "embedding_length": 4096,
                "architecture": "llama",
                "quantization": "Q4_0",
                "rope_frequency_base": 1e6
            },
            default_system_prompt="You are a helpful programming assistant."
        ),
        "neural-chat": ModelConfig(
            name="Neural Chat",
            size=7.2,  # 7.2B parameters
            category="Conversation",
            strengths=[
                "Conversação natural",
                "Manutenção de contexto",
                "Respostas empáticas",
                "Interação social"
            ],
            capabilities=[
                "Atendimento ao usuário",
                "Explicações didáticas",
                "Interações sociais",
                "Suporte contextual"
            ],
            parameters={
                "temperature": 0.8,
                "top_p": 0.9,
                "context_length": 32768,
                "embedding_length": 4096,
                "architecture": "llama",
                "quantization": "Q4_0",
                "num_ctx": 4096
            },
            default_system_prompt="You are a friendly and helpful conversational assistant."
        ),
        "orca-mini": ModelConfig(
            name="Orca Mini",
            size=3.4,  # 3.4B parameters
            category="Lightweight",
            strengths=[
                "Respostas rápidas",
                "Baixo consumo de recursos",
                "Tarefas simples",
                "Eficiência computacional"
            ],
            capabilities=[
                "Respostas curtas",
                "Consultas básicas",
                "Tarefas de baixa complexidade",
                "Processamento rápido"
            ],
            parameters={
                "temperature": 0.7,
                "top_p": 0.9,
                "context_length": 2048,
                "embedding_length": 3200,
                "architecture": "llama",
                "quantization": "Q4_0"
            },
            default_system_prompt="You are an AI assistant that follows instruction extremely well. Help as much as you can."
        ),
        "llama3.2": ModelConfig(
            name="LLaMA 3.2",
            size=3.2,  # 3.2B parameters
            category="Lightweight",
            strengths=[
                "Balanço entre performance e tamanho",
                "Eficiência computacional",
                "Respostas rápidas",
                "Grande contexto"
            ],
            capabilities=[
                "Processamento de texto básico",
                "Geração de conteúdo simples",
                "Tarefas gerais leves",
                "Análise de documentos longos"
            ],
            parameters={
                "temperature": 0.7,
                "top_p": 0.9,
                "context_length": 131072,
                "embedding_length": 3072,
                "architecture": "llama",
                "quantization": "Q4_K_M"
            }
        )
    })
    favorite_models: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize derived settings after instantiation."""
        # Ensure data directory exists
        if isinstance(self.data_dir, str):
            self.data_dir = Path(self.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set db_path if not provided
        if self.db_path is None:
            self.db_path = self.data_dir / "chat.db"
        elif isinstance(self.db_path, str):
            self.db_path = Path(self.db_path)
        
        # Set log file if not provided
        if self.log_file is None:
            self.log_file = self.data_dir / "app.log"
        elif isinstance(self.log_file, str):
            self.log_file = Path(self.log_file)
    
    def save(self, path: Optional[Path] = None):
        """Save settings to JSON file."""
        if path is None:
            path = self.data_dir / "settings.json"
        
        # Convert paths to strings for JSON serialization
        data = {
            **self.__dict__,
            "data_dir": str(self.data_dir),
            "db_path": str(self.db_path) if self.db_path else None,
            "log_file": str(self.log_file) if self.log_file else None
        }
        
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    
    @classmethod
    def load(cls, path: Path) -> 'AppSettings':
        """Load settings from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model."""
        return self.model_configs.get(model_name)
    
    def add_favorite_model(self, model_name: str):
        """Add model to favorites."""
        if model_name not in self.favorite_models and model_name in self.model_configs:
            self.favorite_models.append(model_name)
    
    def remove_favorite_model(self, model_name: str):
        """Remove model from favorites."""
        if model_name in self.favorite_models:
            self.favorite_models.remove(model_name)
