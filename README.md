# Contexto

- Este repositório contém o backend (API em Python/FastAPI) do projeto **rd-challenge**. É uma API para controlar sondas em uma malha 2D para o desafio técnico da RD Station. Use as instruções abaixo para executar o projeto em desenvolvimento.

## Pré-requisitos

- **Python:** Linguagem da API. Versão >= 3.14
- **uv:** Gerenciador de pacotes uv (utilizado para este projeto).

## Dependências principais

- **FastAPI:** framework web para construir a API. Versão: >= 0.136.3
- **Uvicorn:** servidor ASGI para rodar a aplicação. Versão: >= 0.48.0
- **pytest:** framework de testes para validar a API. Versão: >= 9.0.3
- **httpx:** cliente HTTP assíncrono para testes de integração. Versão: >= 0.28.1
- **anyio:** biblioteca de suporte para operações assíncronas. Versão: >= 4.13.0
- **ruff:** ferramenta de linter para manter a qualidade do código. Versão: >= 0.15.14

## API

- **Localização:** [src/app/main.py](src/app/main.py)
- **Instalar dependências:**
  - Crie e ative um virtual env na raiz do projeto: uv venv (Windows: .venv\Scripts\activate)
  - Atualize e instale os pacotes a partir do pyproject.toml:
    uv sync
- **Rodar em desenvolvimento:**
  - Na raiz do projeto, execute o Uvicorn apontando para o diretório src:
    uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
  - A API ficará disponível em <http://127.0.0.1:8000>.
- **Rodar Testes:**
  - A suíte de testes usa pytest e está configurada para reconhecer a estrutura src/. Para testar rode o comando:
    pytest

## Recomendações rápidas

- Acesse <http://127.0.0.1:8000/docs> logo após subir a aplicação para testar e validar a API manualmente pelo Swagger UI.
- Utilize a versão das dependências listadas em *Dependências principais* e também no arquivo `pyproject.toml` para garantir compatibilidade e evitar erros.
