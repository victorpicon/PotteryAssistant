import os
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from pydantic import BaseModel

from pottery_assistant.agent import create_agent

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with AsyncRedisSaver.from_conn_string(REDIS_URL) as checkpointer:
        await checkpointer.asetup()
        app.state.agent = create_agent(checkpointer)
        yield


app = FastAPI(
    title="Pottery Assistant",
    description="Agente de IA para auxiliar alunos de aula de cerâmica",
    version="0.0.1",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        result = await app.state.agent.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    last_message = result["messages"][-1]
    return ChatResponse(response=last_message.content, session_id=session_id)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
