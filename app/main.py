"""FastAPI Memory Agent Application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.routes import router as api_router
from .api.websocket import router as websocket_router
from .middleware.logging import LoggingMiddleware
from utils.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Asis Memory Agent API server")
    yield
    # Shutdown
    logger.info("Shutting down Asis Memory Agent API server")


# Create FastAPI application
app = FastAPI(
    title="Asis Memory Agent API",
    description="Production-ready memory agent with LangGraph",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(api_router, prefix="/api/v1", tags=["api"])
app.include_router(websocket_router, tags=["websocket"])


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return JSONResponse({
        "message": "Asis Memory Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
        "metrics": "/api/v1/metrics",
        "websocket": "/ws/chat"
    })


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )
