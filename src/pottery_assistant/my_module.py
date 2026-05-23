import os

import uvicorn


def run_from_script() -> None:
    dev = os.getenv("ENV", "development") != "production"
    uvicorn.run(
        "pottery_assistant.api:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=dev,
    )
