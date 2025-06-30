from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import health
from src.routers.v1 import logged_time
from src.utils import setup_logging

from src.float import FloatClient
from fastmcp import FastMCP

import os

logger = setup_logging()

ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

FLOAT_ACCESS_TOKEN = os.getenv("FLOAT_ACCESS_TOKEN")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """Manages the startup and shutdown events for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.state.float_client = FloatClient(
        access_token=FLOAT_ACCESS_TOKEN,
        application_name="Float MCP Server",
        contact_email="float_mcp@example.com",
    )

    yield


api_app = FastAPI(title="Float API Server", lifespan=lifespan)
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=ALLOW_METHODS,
    allow_headers=["*"],
)
api_app.include_router(health.router)
api_app.include_router(logged_time.router, prefix="/v1")

mcp_app = FastMCP.from_fastapi(api_app).http_app(stateless_http=True)

app = FastAPI(
    title="Float MCP",
    lifespan=mcp_app.lifespan,
)

app.mount("/mcp", mcp_app)  # mcp is at /mcp
app.mount("/", api_app)
