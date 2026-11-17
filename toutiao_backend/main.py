"""应用入口：创建 FastAPI 实例。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

import models  # noqa: F401  确保 ORM 模型已注册到 Base.metadata
from config.db_conf import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 开发阶段自动建表；生产环境请改用 Alembic 迁移
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="头条项目 API", version="0.1.0", lifespan=lifespan)

# 在这里注册你自己的路由，例如：
# from routers.news import router as news_router
# app.include_router(news_router, prefix="/api")


@app.get("/", tags=["健康检查"])
async def health():
    return {"status": "ok"}
