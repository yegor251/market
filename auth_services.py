import jwt
from utils import utility_service
from CVAR import SECRET_KEY, ALGORITHM
from users import user_manager
from sessions_manager import manage_session
from db import db_manager


class Services:
    @staticmethod
    async def login(request):
        user = await db_manager.get_user(request.username)
        if user and utility_service.verify_password(request.password, user["password"]):
            token = utility_service.create_access_token(data={"sub": request.username})
            user = user_manager.read_user(request.username)
            return {"status": True, "access_token": token, "token_type": "bearer", "user": user}
        else:
            return {"status": False, "error_type": "Invalid username or password"}

    @staticmethod
    async def register(request):
        user = await db_manager.get_user(request.username)
        if user:
            if utility_service.verify_password(request.password, user["password"]):
                token = utility_service.create_access_token(data={"sub": request.username})
                usr = user_manager.get_user(request.username)
                return {"status": True, "access_token": token, "token_type": "bearer", "user": usr}
            else:
                return {"status": False, "error_type": "Login is taken"}
        else:
            await db_manager.add_user(request.username, request.password)
            token = utility_service.create_access_token(data={"sub": request.username})
            manage_session(request.username)
            user = user_manager.read_user(request.username)
            return {"status": True, "access_token": token, "token_type": "bearer", "user": user}

    @staticmethod
    async def logout(request):
        try:
            payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return {"status": False}
            user_manager.save_user(username)
        except jwt.ExpiredSignatureError:
            return {"status": False}
        except Exception:
            return {"status": False}

    @staticmethod
    async def get_current_user(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return {"status": False}
            return {"status": True, "username": username}
        except jwt.ExpiredSignatureError:
            return {"status": False}
        except Exception:
            return {"status": False}

    @staticmethod
    async def claim_bonus(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return {"status": False}

            flag, sec = user_manager.can_gen_bonus(username)
            if flag:
                money = utility_service.gen_daily_bonus()
                user_manager.get_bonus(username, money)
                user = user_manager.get_user(username)
                return {"status": True, "user": user}
            else:
                return {"status": False, "sec": sec}
        except jwt.ExpiredSignatureError:
            return {"status": False}
        except Exception:
            return {"status": False}

    @staticmethod
    async def purchase_item(request):
        try:
            payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return {"status": False}

            if user_manager.buy_item(request.item_id, username):
                return {"status": True}
            else:
                return {"status": False}
        except jwt.ExpiredSignatureError:
            return {"status": False}
        except Exception:
            return {"status": False}


service = Services()
