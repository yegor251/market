from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    status: bool
    access_token: str | None = None
    token_type: str | None = None
    user: dict | None = None
    error_type: str | None = None
    sec: int | None = None

class BuyItemRequest(BaseModel):
    item_id: str
    token: str