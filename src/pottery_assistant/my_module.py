import uvicorn


def run_from_script() -> None:
    uvicorn.run(
        "pottery_assistant.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
