"""数据库配置：异步引擎、Session 工厂、ORM 基类、FastAPI 依赖。"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # toutiao_project/
BACKEND_ROOT = Path(__file__).resolve().parents[1]  # toutiao_backend/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # 两处 .env 都会读取，后面的优先；也支持系统环境变量
        env_file=(PROJECT_ROOT / ".env", BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "mysql+aiomysql://root:@localhost:3306/toutiao?charset=utf8mb4"


settings = Settings()

engine = create_async_engine(settings.database_url, echo=True, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


async def get_db():
    """FastAPI 依赖：每个请求一个独立的数据库会话。"""
    async with AsyncSessionLocal() as session:
        yield session
