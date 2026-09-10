from datetime import date
from pathlib import Path
from .database import SessionLocal
from .repository.service_repository import ServiceRepository


LINES = [
    "16:42:31 ERROR [user-service] 用户登录失败，userId: 10086，ip: 10.1.2.3 traceId=8d4f2c3c9a7b4e1f9c3d9e0a8b6f7c3e",
    "16:42:28 WARN [order-service] 订单创建失败，orderId: 202409120001，isPaid: false traceId=6a7b3c9d8e2f4d6b1c3ff9e0a8b2c8d1",
    "16:42:26 INFO [user-service] 用户注册成功，userId: 10087 traceId=d4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4",
    "16:42:23 INFO [payment-service] 支付成功，amount: 199.00 traceId=7c6d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3",
    "16:42:17 ERROR [gateway] 请求超时，目标服务：order-service traceId=9e8f7d6b5c4aa3e2f1d0c9b8a7f6e5d4c3",
    "16:42:13 WARN [user-service] 用户身份校验丢失，userId: 10086 traceId=a8b1c2a3e4f5a6b7c8d9e0f1a2b3c4d5",
    "16:42:07 INFO [system] 系统启动完成，耗时：2.45s traceId=3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9",
    "16:42:03 ERROR [order-service] 订单状态更新失败 traceId=1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7",
    "16:41:58 INFO [user-service] 获取用户信息成功 traceId=2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
    "16:41:52 WARN [payment-service] 金额不足，amount: 500.00 traceId=d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1",
    "16:41:46 INFO [order-service] 订单取消成功 traceId=4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
    "16:41:39 ERROR [gateway] 连接超时，服务：payment-service traceId=9f8e7d6c5b4a3e2f1d0c9b8a7f6e5d4c3",
]


def seed_demo_data():
    runtime = Path(__file__).resolve().parent.parent / "runtime_logs"
    runtime.mkdir(exist_ok=True)
    k8s_runtime = runtime / "k8s"
    k8s_runtime.mkdir(exist_ok=True)
    for day in {date.today().isoformat(), "2026-09-07"}:
        path = runtime / f"app-{day}.log"
        if not path.exists(): path.write_text("\n".join(f"{day} {line}" for line in LINES) + "\n", encoding="utf-8")
    previous = runtime / "app-2026-09-06.log"
    if not previous.exists():
        old = [f"2026-09-06 15:00:{i:02d} ERROR [gateway] 昨日错误 {i} traceId=old-error-{i}" for i in range(7)]
        old += [f"2026-09-06 15:01:{i:02d} WARN [orders] 昨日警告 {i} traceId=old-warn-{i}" for i in range(5)]
        previous.write_text("\n".join(old) + "\n", encoding="utf-8")
    defaults = [
        dict(service_name="生产环境应用日志", log_path=str(runtime), source_type="app", enabled=True, status="collecting"),
        dict(service_name="Kubernetes 集群日志", log_path=str(k8s_runtime), source_type="k8s", enabled=True, status="collecting"),
        dict(service_name="阿里云 SLS", log_path=str(runtime / "unavailable"), source_type="cloud", enabled=True, status="error"),
        dict(service_name="测试环境日志", log_path=str(runtime / "test"), source_type="test", enabled=False, status="disabled"),
    ]
    with SessionLocal() as db:
        if not ServiceRepository.list(db):
            for values in defaults:
                ServiceRepository.create(db, **values)
