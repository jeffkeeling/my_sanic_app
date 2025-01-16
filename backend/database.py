# backend/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to your project's root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get database configuration from environment variables
DATABASE_DIR = os.path.join(BASE_DIR, os.getenv('DATABASE_DIR', 'data'))
DATABASE_NAME = os.getenv('DATABASE_NAME', 'users.db')
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)

# Ensure data directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Construct database URL
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

logger.info(f"Database path: {DATABASE_PATH}")
logger.info(f"Database URL: {DATABASE_URL}")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    try:
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_session():
    return async_session()