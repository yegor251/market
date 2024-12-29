import asyncpg
from fastapi import HTTPException
from CVAR import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def initialize_pool(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(**DB_CONFIG)

    async def close_pool(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def get_pool(self):
        if self.pool is None:
            raise HTTPException(status_code=500, detail="Database pool is not initialized.")
        return self.pool

    async def get_user(self, username: str):
        if not self.pool:
            raise HTTPException(status_code=500, detail="Database pool is not initialized.")

        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT username, password FROM market_users WHERE username = $1", username
            )
            return dict(user) if user else None

    async def add_user(self, username: str, password: str):
        if not self.pool:
            raise HTTPException(status_code=500, detail="Database pool is not initialized.")

        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO market_users (username, password) VALUES ($1, $2)", username, password
            )


db_manager = DatabaseManager()
