from jwt import decode, ExpiredSignatureError
from config import settings
from .utils import utility_service
from .user_manager import user_manager
from models.schemas import *

class TokenService:
    @staticmethod
    def create_auth_response(username: str) -> TokenResponse:
        token = utility_service.create_access_token(data={"sub": username})
        user_data = user_manager.read_user(username)
        return TokenResponse(
            status=True,
            access_token=token,
            token_type="bearer",
            user=user_data
        )

    @staticmethod
    def decode_token(token: str):
        try:
            payload = decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload.get("sub")
        except ExpiredSignatureError:
            return None
        except Exception:
            return None

token_service = TokenService()