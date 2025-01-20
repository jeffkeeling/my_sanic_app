import asyncio
import os
from database import engine, Base
from seed import seed_database

async def reset_database():
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Recreate and seed
    await seed_database()

if __name__ == "__main__":
    asyncio.run(reset_database())