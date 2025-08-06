from fastapi import FastAPI

from src.routes import accounts, movies

app = FastAPI(
    title="Online Cinema",
    description="A platform to watch and purchase movies online.",
    version="0.1.0"
)


api_v1_prefix = "/api/v1"

app.include_router(accounts.router, prefix=f"{api_v1_prefix}/accounts", tags=["accounts"])
app.include_router(movies.router, prefix=f"{api_v1_prefix}/theater", tags=["theater"])


@app.get("/health", tags=["System"])
def health_check():
    """
    A simple endpoint to check if the service is running.
    """
    return {"status": "ok"}
