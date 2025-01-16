# backend/test_db.py
import asyncio
import logging
from database import init_db, get_session, Base, engine
from api.models import User
from sqlalchemy import text
from sqlalchemy.future import select

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database():
    try:
        # Initialize the database and create tables
        logger.info("Initializing database...")
        await init_db()
        
        # Get a database session
        logger.info("Creating test user...")
        async for session in get_session():
            try:
                # Create a test user
                test_user = User(
                    name="Test User",
                    email="test@example.com"
                )
                session.add(test_user)
                await session.commit()
                logger.info(f"Created test user: {test_user.to_dict()}")
                
                # Query the user back
                logger.info("Querying users...")
                result = await session.execute(select(User))
                users = result.scalars().all()
                
                # Print results
                for user in users:
                    logger.info(f"Found user: {user.to_dict()}")
            except Exception as e:
                await session.rollback()
                logger.error(f"Error in test_database: {e}")
                raise e

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

async def verify_tables():
    logger.info("Verifying database tables...")
    async with engine.connect() as conn:
        try:
            # Use text() for raw SQL queries
            result = await conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            # Remove await from fetchall()
            tables = result.fetchall()
            if not tables:
                logger.info("No tables found in database")
            else:
                logger.info("Tables in database:")
                for table in tables:
                    logger.info(f"- {table[0]}")
        except Exception as e:
            logger.error(f"Error in verify_tables: {e}")
            raise

if __name__ == "__main__":
    try:
        # Run the async functions
        logger.info("Starting database test...")
        asyncio.run(verify_tables())
        asyncio.run(test_database())
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise