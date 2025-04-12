from services import utility_service
from services.token_service import token_service
from services.session_manager import manage_session
from db import db_manager
from services.user_manager import user_manager
from models.schemas import *


class AuthService:
    @staticmethod
    async def _authenticate_user(username: str, password: str):
        user = await db_manager.get_user(username)
        if user and utility_service.verify_password(password, user["password"]):
            return True
        return False

    @staticmethod
    async def login(request: LoginRequest) -> TokenResponse:
        if await AuthService._authenticate_user(request.username, request.password):
            return token_service.create_auth_response(request.username)
        return TokenResponse(status=False, error_type="Invalid username or password")

    @staticmethod
    async def register(request: LoginRequest) -> TokenResponse:
        if await AuthService._authenticate_user(request.username, request.password):
            return token_service.create_auth_response(request.username)

        if await db_manager.get_user(request.username):
            return TokenResponse(status=False, error_type="Login is taken")

        await db_manager.add_user(request.username, request.password)
        manage_session(request.username)
        return token_service.create_auth_response(request.username)

    @staticmethod
    async def logout(request: TokenRequest) -> TokenResponse:
        if username := token_service.decode_token(request.token):
            user_manager.save_user(username)
            return TokenResponse(status=True)
        return TokenResponse(status=False)

    @staticmethod
    async def claim_bonus(token: str) -> TokenResponse:
        if not (username := token_service.decode_token(token)):
            return TokenResponse(status=False)

        flag, sec = user_manager.can_gen_bonus(username)
        if flag:
            money = utility_service.gen_daily_bonus()
            user_manager.get_bonus(username, money)
            return TokenResponse(status=True, user=user_manager.get_user(username))
        return TokenResponse(status=False, sec=sec)

    @staticmethod
    async def purchase_item(request: BuyItemRequest) -> TokenResponse:
        if not (username := token_service.decode_token(request.token)):
            return TokenResponse(status=False)

        if user_manager.buy_item(request.item_id, username):
            return TokenResponse(status=True)
        return TokenResponse(status=False)


auth_service = AuthService()