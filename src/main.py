from fastapi import FastAPI
from src.routes import (
    accounts
)
app = FastAPI(
    title="Online Cinema",
    description="A platform to watch and purchase movies online.",
    version="0.1.0"
)

api_v1_prefix = "/api/v1"

app.include_router(accounts.router, prefix=f"{api_v1_prefix}/accounts", tags=["accounts"])


@app.get("/health", tags=["System"])
def health_check():
    """
    A simple endpoint to check if the service is running.
    """
    return {"status": "ok"}

