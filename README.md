# Contexto

- Este repositório contém o backend (API em Python/FastAPI) do projeto **rd-challenge**. É uma API para controlar sondas em uma malha 2D para o desafio técnico da RD Station. Use as instruções abaixo para executar o projeto em desenvolvimento.

## Pré-requisitos

- **Python:** Linguagem da API. Versão >= 3.14
- **uv:** Gerenciador de pacotes uv (utilizado para este projeto).
- **PostgreSQL:** Banco de dados utilizado para persistência.
- **Docker:** Caso prefira rodar a aplicação contêinerizada.

## API

### Configurando e Rodando com Docker

- Certifique-se de que o Docker e o Docker Compose estejam instalados e em execução.
- Configure as variáveis de ambiente no arquivo `.env` conforme necessário, especialmente as relacionadas ao banco de dados PostgreSQL (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`). Note que a variável `POSTGRES_SERVER` será ignorada quando rodar com Docker, pois a aplicação se conectará automaticamente ao serviço `db` definido no `docker-compose.yml`.
- Na raiz do projeto, execute o comando: `docker compose up --build`
- O Docker irá construir as imagens necessárias e iniciar os contêineres para a API e o banco de dados PostgreSQL.
- A API estará disponível em <http://localhost:8000> e o banco de dados PostgreSQL estará acessível para a aplicação.
- Para acessar a documentação interativa da API, vá para <http://localhost:8000/docs>.
- Para rodar os testes dentro do contêiner, use:
  - Windows: `docker compose run --rm -v "%cd%/htmlcov:/app/htmlcov" api pytest --cov=src --cov-report=html`.
  - Linux/Mac: `docker compose run --rm -v "$(pwd)/htmlcov:/app/htmlcov" api pytest --cov=src --cov-report=html`.

### Configuração Manual e Rodando Localmente

- Certifique-se de ter o Python e o PostgreSQL instalados e configurados corretamente em sua máquina.
- Configure as variáveis de ambiente no arquivo `.env` conforme necessário, especialmente as relacionadas ao banco de dados PostgreSQL (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SERVER`, `POSTGRES_DB`).
- **Na raiz do projeto, crie um ambiente virtual e instale as dependências usando o `uv`**:
  - Crie o virtual env: `uv venv`
  - Ative o virtual env:
    - Windows: `uv venv activate`
    - Linux/Mac: `source .venv/bin/activate`
  - Atualize e instale os pacotes a partir do `pyproject.toml`:
    `uv sync`
- Na raiz do projeto, entre em `src/` e execute `python run_server.py` para iniciar a aplicação.
- A API ficará disponível em <http://127.0.0.1:8000>.
- A aplicação tentará criar as tabelas no banco de dados automaticamente na inicialização (lifespan).
- Para acessar a documentação interativa da API, vá para <http://127.0.0.1:8000/docs>.
- Para rodar os testes, execute `pytest` na raiz do projeto. Para ver a cobertura de testes, use `pytest --cov=src --cov-report=html` e acesse o relatório em `htmlcov/index.html`.

## Decisões de implementação

- **Estrutura do projeto:**: Foi o ponto que mais me levou tempo para decidir e que teve mais mudanças durante o desenvolvimento. Optei por uma arquitetura de camadas ao invés de DDD, pois como não teve muitas regras de negócio complexas e distintas, acredito que o encapsulamento em camadas (routers, services, repositories) foi suficiente para manter a organização e a separação de responsabilidades.
- **FastAPI:**: Optei pela simplicidade e por já ter experiência sólida, além de possuir uma integração completa com `Swagger`, o que facilita a documentação e testes manuais.
- **SQLModel:**: Escolhi `SQLModel` por ser uma camada de abstração leve em comparação com o `SQLAlchemy` puro (escolha inicial) e por integrar bem com `Pydantic`, facilitando a definição de modelos de dados e a validação. Outro ponto, é por ser mais fácil configurar funções assíncronas nele.
- **PostgreSQL:**: Tinha iniciado com `SQLite` para o desenvolvimento, porém optei por migrar para o `PostgreSQL`, pela robustez e pela facilidade de configuração usando Docker, além de ser um banco mais adequado para produção.
- **Testes:**:
  -- Motivo: Usei pytest para os testes pela simplicidade de configurar igual o **FastAPI**.
  -- AAA: Adotei a estrutura Arrange-Act-Assert para organizar os testes com poucas exceções como o `test_lifespan`
- **Docker:**: Terminando de configurar a aplicação, optei por adicionar o **Docker** para garantir o profissionalismo do projeto e por já ter a ideia completa das ferramentas que eu iria utilizar, o que facilitou a configuração do `Dockerfile` e do `docker-compose.yml`.
- **Lifespan:**: Descobri o recurso de `lifespan` do FastAPI durante o desenvolvimento e decidi utilizá-lo para criar as tabelas no banco de dados na função `init_db` automaticamente na inicialização da aplicação, garantindo que a estrutura necessária esteja sempre pronta para uso.
- **Configurações de ambiente:**: Optei por usar o `python-dotenv` por já ter conhecimento da solução e por achar bem elegante.
- **Ruff:**: Adicionei o `ruff`, pois acredito que todo projeto precisa ter um reforçador de qualidade de código, e o `ruff` é uma ferramenta moderna e eficiente para isso, além de ser fácil de configurar e usar.

## Dependências principais

- **FastAPI:** framework web para construir a API. Versão: >= 0.136.3
- **Uvicorn:** servidor ASGI para rodar a aplicação. Versão: >= 0.48.0
- **SQLModel:** ORM baseado em SQLAlchemy e Pydantic para interação com o banco de dados. Versão: >= 0.0.38
- **asyncpg / psycopg2-binary:** drivers de conexão com o banco de dados PostgreSQL. Versões: asyncpg >= 0.31.0, psycopg2-binary >= 2.9.12
- **python-dotenv:** gerenciamento de variáveis de ambiente. Versão: >= 1.2.2
- **pytest:** framework de testes para validar a API. Versão: >= 9.0.3
- **httpx:** cliente HTTP assíncrono para testes de integração. Versão: >= 0.28.1
- **anyio:** biblioteca de suporte para operações assíncronas. Versão: >= 4.13.0
- **ruff:** ferramenta de linter para manter a qualidade do código. Versão: >= 0.15.14
- **pytest-cov:** plugin para medir a cobertura dos testes. Versão: >= 7.1.0
- **pytest-asyncio:** plugin para rodar testes assíncronos com pytest. Versão: >= 1.4.0

## Recomendações rápidas

- Utilize a versão das dependências listadas em *Dependências principais* e também no arquivo `pyproject.toml` para garantir compatibilidade e evitar erros.
