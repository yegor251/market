from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth.router import auth_router
from db import db_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["auth"])

@app.on_event("startup")
async def startup_event():
    await db_manager.initialize_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close_pool()