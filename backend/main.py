from backend.utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import foo, files
from backend.config.database import create_tables

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from backend.utils.app_exceptions import app_exception_handler

create_tables()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],  # Allos CORS from the Angular app (Replace with AUTH/ JWT)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(foo.router)
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
