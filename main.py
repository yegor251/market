from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import LoginRequest, TokenRequest, BuyItemRequest
from auth_services import service
from db import db_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await db_manager.initialize_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close_pool()


@app.post("/login")
async def login(request: LoginRequest):
    return await service.login(request)


@app.post("/register")
async def register(request: LoginRequest):
    return await service.register(request)


@app.post("/log-close")
async def log_close(request: TokenRequest):
    await service.logout(request)


@app.get("/dailybonus")
async def get_daily_bonus(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization token is missing")

    token = authorization.split("Bearer ")[-1]
    return await service.claim_bonus(token)


@app.post("/buy_item")
async def buy_item(request: BuyItemRequest):
    return await service.purchase_item(request)
