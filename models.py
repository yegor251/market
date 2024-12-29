from pydantic import BaseModel

# Модель данных для логина
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenRequest(BaseModel):
    token: str

class BuyItemRequest(BaseModel):
    item_id: str
    token: str