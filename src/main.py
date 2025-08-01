from fastapi import FastAPI
from src.config.settings import settings

# --- Routers ---
# We will uncomment these lines as we create the routers in the next steps
# from src.routes import accounts, movies, profiles

app = FastAPI(
    title="Online Cinema",
    description="A platform to watch and purchase movies online.",
    version="0.1.0"
)

# --- API v1 Prefix ---
api_v1_prefix = "/api/v1"

# --- Include Routers ---
# We will add the routers to the app in the upcoming steps
# app.include_router(accounts.router, prefix=f"{api_v1_prefix}/accounts", tags=["accounts"])
# app.include_router(profiles.router, prefix=f"{api_v1_prefix}/profiles", tags=["profiles"])
# app.include_router(movies.router, prefix=f"{api_v1_prefix}/theater", tags=["theater"])


@app.get("/health", tags=["System"])
def health_check():
    """
    A simple endpoint to check if the service is running.
    """
    return {"status": "ok"}

