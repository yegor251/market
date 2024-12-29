import random
import jwt
from datetime import datetime, timedelta
from CVAR import SECRET_KEY, ALGORITHM


class UtilityService:
    @staticmethod
    def gen_daily_bonus():
        return random.randint(50, 200)

    @staticmethod
    def create_access_token(data: dict):
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_password(plain_password, stored_password):
        return plain_password == stored_password


utility_service = UtilityService()
