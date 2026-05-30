# Contexto

- Este repositório contém o backend (API em Python/FastAPI) do projeto **rd-challenge**. É uma API para controlar sondas em uma malha 2D para o desafio técnico da RD Station. Use as instruções abaixo para executar o projeto em desenvolvimento.

## Pré-requisitos

- **Python:** Linguagem da API. Versão >= 3.14
- **uv:** Gerenciador de pacotes uv (utilizado para este projeto).
- **PostgreSQL:** Banco de dados utilizado para persistência.
- **Ferramenta de gerenciamento de banco de dados:** Opcional, mas recomendado para facilitar a visualização dos dados. Utilizei tanto o `pgAdmin` quanto o `DBeaver` durante o desenvolvimento.
- **API Client:** Para testar os endpoints da API, como o `Postman`, `Insomnia` ou usar o próprio `Swagger UI` (recomendado).
- **Docker:** Caso prefira rodar a aplicação contêinerizada.

## API

### Configurando e Rodando com Docker

- Certifique-se de que o Docker está instalado e rodando em sua máquina.
- Configure as variáveis de ambiente:
  - Crie um arquivo `.env` na raiz do projeto (ou copie o `.env.example`) e preencha as variáveis de ambiente necessárias para o banco de dados PostgreSQL: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD`.
  - Caso deseje usar o pgAdmin para gerenciar o banco de dados, configure as variáveis: `PGADMIN_DEFAULT_EMAIL` e `PGADMIN_DEFAULT_PASSWORD`.
- Na raiz do projeto, execute o comando: `docker compose up --build`
- O Docker irá construir as imagens necessárias e iniciar os contêineres para a API e o banco de dados PostgreSQL.
- **URLS:**
  - API: <http://localhost:8000/api/v1>
  - Documentação interativa da API: <http://localhost:8000/docs>
  - PGAdmin: <http://localhost:5050> (use as credenciais do `.env` para login)
- **Testes:**
  - Para rodar os testes, use o comando:
    - Windows: `docker compose run --rm api pytest`
    - Linux/Mac: `docker compose run --rm api pytest`
  - Para rodar os testes e também gerar o relatório de cobertura, execute:
    - Windows: `docker compose run --rm -v "%cd%/htmlcov:/app/htmlcov" api pytest --cov=src --cov-report=html`.
    - Linux/Mac: `docker compose run --rm -v "$(pwd)/htmlcov:/app/htmlcov" api pytest --cov=src --cov-report=html`.

### Configuração Manual e Rodando Localmente

- Certifique-se de ter o Python e o PostgreSQL instalados e configurados corretamente em sua máquina.
- Configure as variáveis de ambiente no arquivo `.env` conforme necessário, especialmente as relacionadas ao banco de dados PostgreSQL (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SERVER`, `POSTGRES_DB`).
- Na raiz do projeto, crie um ambiente virtual e instale as dependências usando o `uv`:
  - Crie o virtual env: `uv venv`
  - Ative o virtual env:
    - Windows: `uv venv activate`
    - Linux/Mac: `source .venv/bin/activate`
  - Atualize e instale os pacotes a partir do `pyproject.toml`:
    `uv sync`
- Na raiz do projeto, entre em `src/` e execute `python run_server.py` para iniciar a aplicação.
- A aplicação tentará criar as tabelas no banco de dados automaticamente na inicialização (lifespan).
- **URLS**:
  - API: <http://127.0.0.1:8000/api/v1>
  - Documentação interativa da API: <http://127.0.0.1:8000/docs>
- **Testes**:
  - Para rodar os testes execute `pytest` na raiz do projeto.
  - Para rodar os testes e também gerar o relatório de cobertura, execute: `pytest --cov=src --cov-report=html` e acesse o relatório em `htmlcov/index.html`.

### Endpoints

- `GET /api/v1/`: Endpoint de health check para verificar se a API está funcionando.
- `POST /api/v1/launch-probe`: Endpoint para lançar uma nova sonda
  - **Requisição**:

    ```json
    {"x": "int", "y": "int", "direction": "str"}
    ```

  - **Resposta**:

    ```json
    {"id": "int", "x": "int", "y": "int", "direction": "str"}
    ```

- `POST /api/v1/move-probe/{probe_id}/`: Endpoint para mover uma sonda existente
  - **Requisição**:

    ```json
    {"commands": "str"}
    ```

  - **Resposta**:

    ```json
    {"id": "int", "x": "int", "y": "int", "direction": "str"}
    ```

- `GET /api/v1/probes/`: Endpoint para listar todas as sondas lançadas
  - **Resposta**:

    ```json
    [{"id": "int", "x": "int", "y": "int", "direction": "str"}, "..."]
    ```

## Recomendações rápidas

- Utilize a versão das dependências listadas em *Dependências principais* e também no arquivo `pyproject.toml` para garantir compatibilidade e evitar erros.
- Ao usar o `PGAdmin` quando for adicionar um novo servidor de banco de dados, use as seguintes configurações:
  - Host: `db` (nome do serviço do banco de dados no Docker)
  - Port: `5432`
  - Maintenance database: `POSTGRES_DB`
  - Username: `POSTGRES_USER`
  - Password: `POSTGRES_PASSWORD`

## Decisões de implementação

- **Estrutura do projeto:** Foi o ponto que mais me levou tempo para decidir e que teve mais mudanças durante o desenvolvimento. Optei por uma arquitetura de camadas ao invés de DDD, pois como não teve muitas regras de negócio complexas e distintas, acredito que o encapsulamento em camadas (routers, services, repositories) foi suficiente para manter a organização e a separação de responsabilidades.
- **FastAPI:** Optei pela simplicidade e pela minha experiência prévia com o `FastAPI`, além de possuir bons logs e uma integração com o Swagger UI para documentação automática, o que facilita a visualização e o teste dos endpoints.
- **SQLModel:**: Escolhi `SQLModel` por ser uma camada de abstração leve em comparação com o `SQLAlchemy` puro (escolha inicial) e por integrar bem com `Pydantic`, facilitando a definição de modelos de dados e a validação. Outro ponto, é por ser mais fácil configurar funções assíncronas nele.
- **PostgreSQL:** Tinha iniciado com `SQLite` para o desenvolvimento, porém optei por migrar para o `PostgreSQL`, pela robustez e pela facilidade de configuração usando Docker, além de ser um banco mais adequado para produção.
- **Testes:**
  - Motivo: Usei pytest para os testes pela simplicidade de configurar igual o **FastAPI**.
  - AAA: Adotei a estrutura Arrange-Act-Assert para organizar os testes com poucas exceções como o `test_lifespan` e o `test_launch_probe_invalid_direction`
- **Docker:** Terminando de configurar a aplicação, optei por adicionar o **Docker** para garantir o profissionalismo do projeto e por já ter a ideia completa das ferramentas que eu iria utilizar, o que facilitou a configuração do `Dockerfile` e do `docker-compose.yml`.
- **Lifespan:** Descobri o recurso de `lifespan` do FastAPI durante o desenvolvimento e decidi utilizá-lo para criar as tabelas no banco de dados na função `init_db` automaticamente na inicialização da aplicação, garantindo que a estrutura necessária esteja sempre pronta para uso.
- **Configurações de ambiente:** Optei por usar o `python-dotenv` por já ter conhecimento da solução e por achar bem elegante.
- **Ruff:** Adicionei o `ruff`, pois acredito que todo projeto precisa ter um reforçador de qualidade de código, e o `ruff` é uma ferramenta moderna e eficiente para isso, além de ser fácil de configurar e usar.
- **Custom exceptions:** Adicionei exceções customizadas para os erros de negócio, pois isso garante que a API possa retornar mensagens de erro mais claras e específicas.
- **PGAdmin:** Adicionei o `pgAdmin` no Docker para facilitar a visualização dos dados e o gerenciamento do banco de dados.
- **Separação de Schema e Model:** Mesmo que o SQLModel permita usar o mesmo modelo para a definição da tabela e para a validação dos dados, optei por separar os `schemas` dos `models` (SQLModel) para encapsular melhor as responsabilidades e evitar acoplamento entre a estrutura do banco de dados e a estrutura dos dados que a API recebe ou retorna.

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
