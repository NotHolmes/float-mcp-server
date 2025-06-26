from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.routers import health
from src.routers.v1 import logged_time
from src.utils import setup_logging

logger = setup_logging()

ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """Manages the startup and shutdown events for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    yield


app = FastAPI(title="Float MCP Server", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=ALLOW_METHODS,
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(logged_time.router, prefix="/v1")


@app.middleware("http")
async def add_custom_data(request: Request, call_next: Callable) -> Response:
    """Middleware to add custom data to each incoming request if it doesn't exist.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The function to call the next middleware in the chain.

    Returns:
        Response: The response object.
    """
    response = await call_next(request)
    return response
