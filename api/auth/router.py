from fastapi import APIRouter, Header, HTTPException
from .service import auth_service
from models.schemas import LoginRequest, TokenRequest, BuyItemRequest, TokenResponse

auth_router = APIRouter()

@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    return await auth_service.login(request)

@auth_router.post("/register", response_model=TokenResponse)
async def register(request: LoginRequest):
    return await auth_service.register(request)

@auth_router.post("/logout", response_model=TokenResponse)
async def logout(request: TokenRequest):
    return await auth_service.logout(request)

@auth_router.get("/dailybonus", response_model=TokenResponse)
async def get_daily_bonus(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    token = authorization.split("Bearer ")[-1]
    return await auth_service.claim_bonus(token)

@auth_router.post("/buy_item", response_model=TokenResponse)
async def buy_item(request: BuyItemRequest):
    return await auth_service.purchase_item(request)