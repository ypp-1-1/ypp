# toutiao_project

基于 FastAPI + SQLAlchemy（异步）+ MySQL 的项目脚手架（仅框架，业务代码自行编写）。

## 目录结构

```
toutiao_project/
├── toutiao_backend/
│   ├── config/
│   │   └── db_conf.py   # 配置（.env）、异步引擎、Session 工厂、Base、get_db
│   ├── models/          # ORM 模型（空，待编写）
│   ├── schemas/         # Pydantic 请求/响应模型（空，待编写）
│   ├── crud/            # 数据访问层（空，待编写）
│   ├── routers/         # 路由层，按业务拆分（空，待编写）
│   ├── utils/           # 通用工具（预留）
│   └── main.py          # FastAPI 实例
├── .env.example         # 环境变量示例
├── .gitignore
├── requirements.txt
└── README.md
```

建议分层调用方向：`routers → crud → models`，`schemas` 负责接口出入参校验。

## 快速开始

```bash
# 1. 激活虚拟环境
.venv\Scripts\activate

# 2. 配置环境变量
copy .env.example .env

# 3. 进入后端目录并启动（导入是相对当前目录的，必须在 toutiao_backend 下运行）
cd toutiao_backend
uvicorn main:app --reload
```

启动后访问：

- 接口文档：http://127.0.0.1:8000/docs
- 健康检查：`GET /` 返回 `{"status": "ok"}`

## 编写业务代码

1. 在 `models/` 下新建 ORM 模型，并在 `models/__init__.py` 中导入，确保建表时被注册。
2. 在 `schemas/` 下定义出入参模型。
3. 在 `crud/` 下封装数据访问函数。
4. 在 `routers/` 下创建 `APIRouter`，然后在 `main.py` 中 `app.include_router(...)` 注册。

## 数据库

默认连接串在 `toutiao_backend/config/db_conf.py`，可通过 `.env` 的 `DATABASE_URL` 覆盖（会依次读取项目根目录和 `toutiao_backend/` 下的 `.env`）：

```
mysql+aiomysql://用户名:密码@主机:3306/库名?charset=utf8mb4
```

注意：SQLAlchemy 不会自动创建数据库，需要先手动建库：

```sql
CREATE DATABASE toutiao CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

`main.py` 的 `lifespan` 会在启动时自动建表，仅适合开发阶段；上线前请改用 Alembic 迁移。

## 下一步

1. 在 `config/db_conf.py` 里接入 Redis / JWT 等配置项
2. 在 `utils/` 下补充密码哈希、鉴权依赖等工具函数
3. 生产部署前引入 Alembic 管理表结构变更
