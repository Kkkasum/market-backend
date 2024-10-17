from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.common import config


engine = create_async_engine(config.DB_URI)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
