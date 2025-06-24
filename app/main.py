from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import flight
from .config import settings
from .data.flightradar import get_usage

app = FastAPI(
    title="Flight API",
    description="A FastAPI application for flight information",
    version="0.1.0",
    debug=settings.APP_DEBUG
)

app.include_router(flight.router, prefix="/api")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Flight API",
        "environment": settings.APP_ENV,
        "debug": settings.APP_DEBUG
    }

@app.get("/usage")
def get_usage_endpoint():
    return {
        "flightradar": get_usage(),
        "opensky": get_usage()
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "debug": settings.APP_DEBUG
    }

