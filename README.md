# AI 日志管理助手

一个面向单机日志目录的轻量级管理工具。前端使用 Vue 3，后端使用 FastAPI；支持 SQLite 本地开发和 Docker Compose + MySQL 部署。

## 功能

- 按日期、等级、关键词、服务和 TraceId 查询日志。
- 读取普通 `.log` 及 gzip 压缩的 `.log.gz` 文件。
- 下载筛选后的原始日志。
- 统计 ERROR、WARN 数量及其同比前一日变化。
- 管理日志服务，定时检查日志目录状态。
- 日志原文不入库；数据库仅保存服务配置、统计及读取位置。

## 项目结构

```text
backend/            FastAPI 后端
  app/              接口、服务、数据模型和日志读取代码
  sql/init.sql      Docker MySQL 首次初始化脚本
  tests/            后端自动化测试
frontend/           Vue 3 前端
sample_logs/        可公开提交的示例日志
docker-compose.yml  CentOS Docker 部署配置
```

## 本地开发

后端默认使用 SQLite。PowerShell 中执行：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

另开一个 PowerShell 运行前端：

```powershell
cd frontend
corepack enable
pnpm install --frozen-lockfile
pnpm run dev
```

页面地址：<http://localhost:5173>

接口文档：<http://127.0.0.1:8000/docs>

## CentOS Docker 部署

部署前创建服务器专用配置，不要提交真实 `.env`：

```bash
cp .env.example .env
vi .env
```

创建日志目录并复制示例日志：

```bash
mkdir -p /var/log/app/demo
cp sample_logs/*.log /var/log/app/demo/
chmod 755 /var/log/app /var/log/app/demo
chmod 644 /var/log/app/demo/*.log
```

检查并启动：

```bash
docker compose config
docker compose up -d --build
docker compose ps
```

页面地址：`http://服务器IP:8080`

首次创建 MySQL 数据卷时，`backend/sql/init.sql` 会自动创建数据库和三张数据表，并登记日志路径为 `/var/log/app/demo` 的示例服务。

宿主机 `/var/log/app` 会只读挂载到后端容器的同一路径(/var/log/app)。真实服务建议分别写入宿主机指定日志目录的子目录，例如：

```text
/var/log/app/user-service
/var/log/app/order-service
/var/log/app/payment-service
```

网页中填写相同的容器路径。后端只允许读取 `ALLOWED_LOG_ROOT` （默认是/var/log/app）指定目录下的文件。

## 配置

根目录 `.env.example` 是 Docker 配置模板：

```env
MYSQL_DATABASE=log_assistant
MYSQL_USER=log_user
MYSQL_PASSWORD=change_this_password
MYSQL_ROOT_PASSWORD=change_this_root_password
```

`backend/.env.example` 是本地直接运行后端时的配置模板。真实 `.env` 需要自己配置。

## 支持的日志格式

```text
2026-09-10 16:42:31 ERROR [user-service] 用户登录失败 traceId=abc123
```

历史日志文件名需要包含 `YYYY-MM-DD` 或 `YYYYMMDD` 日期，例如：

```text
app-2026-09-10.log
app-20260910.log.gz
```

查询当天日志且没有带日期的文件时，会读取目录中的普通 `*.log` 文件。无法解析的非空行会按 INFO 原文返回。

## 测试与构建

后端测试：

```powershell
cd backend
pytest -q
```

前端生产构建：

```powershell
cd frontend
pnpm run build
```

## 使用范围

当前版本适用于可信内网或学习演示环境，尚未提供用户登录和权限控制。对公网部署前，应在反向代理层增加身份认证并限制访问来源。
