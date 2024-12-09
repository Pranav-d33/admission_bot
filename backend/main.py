"""
Main FastAPI Application Entry Point
Configures and runs the chatbot backend service
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from .routers import chat_router
from .database import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered chatbot for Rajasthan Technical Education",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler
    Performs initialization tasks
    """
    try:
        # Verify database connection
        DatabaseManager.get_connection()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler
    Performs cleanup tasks
    """
    logger.info("Application is shutting down")

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global HTTP exception handler
    
    Args:
        request: Incoming request
        exc: HTTP exception
    
    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    
    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )