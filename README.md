# Pottery Assistant

Agente de IA especializado em cerâmica e olaria, criado para tirar dúvidas de alunos de aula de cerâmica. Exposto como API REST com memória de conversa persistida em Redis.

## Tecnologias

- [LangGraph](https://github.com/langchain-ai/langgraph) — orquestração do agente
- [LangChain](https://github.com/langchain-ai/langchain) + Google Gemini — LLM
- [FastAPI](https://fastapi.tiangolo.com) — API REST
- [Redis](https://redis.io) — persistência do histórico de conversa por sessão

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) (para rodar localmente)
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/) (para rodar via container)
- Chave de API do Google (Gemini): [aistudio.google.com](https://aistudio.google.com)

## Configuração

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

| Variável | Descrição | Padrão |
|---|---|---|
| `GOOGLE_API_KEY` | Chave da API do Google Gemini | — |
| `REDIS_URL` | URL de conexão com o Redis | `redis://localhost:6379` |

## Como rodar

### Com Docker (recomendado)

```bash
docker compose up --build
```

### Localmente

Suba o Redis primeiro:

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

Instale as dependências e inicie o servidor:

```bash
uv sync
uv run pottery_assistant
```

A API estará disponível em `http://localhost:8000`.

## API

### `POST /chat`

Envia uma mensagem ao agente. O `session_id` é opcional — se omitido, uma nova sessão é criada automaticamente. Reutilize o mesmo `session_id` para continuar uma conversa.

**Request:**
```json
{
  "message": "Como evito rachaduras na minha peça?",
  "session_id": "opcional-para-continuar-conversa"
}
```

**Response:**
```json
{
  "response": "Rachaduras geralmente acontecem quando...",
  "session_id": "uuid-da-sessao"
}
```

### `GET /health`

Retorna `{"status": "ok"}` quando o serviço está no ar.

### Documentação interativa

Acesse `http://localhost:8000/docs` para a interface Swagger com todos os endpoints.
