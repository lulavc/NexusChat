# Ollama Chat GUI

Uma interface gráfica para interação com modelos Ollama locais.

## Estrutura do Projeto

```
ollama_chat/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação do projeto
├── gui/                   # Componentes da interface gráfica
├── backend/               # Serviços e lógica de backend
├── models/               # Modelos de dados
└── utils/                # Utilitários e configurações
```

## Requisitos

- Python 3.8+
- Ollama instalado e configurado localmente
- Dependências listadas em requirements.txt

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`

## Uso

Execute o programa com:
```bash
python main.py
```
