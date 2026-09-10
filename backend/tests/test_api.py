from fastapi.testclient import TestClient
from app.main import app


def test_health_and_service_crud():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}
        response = client.post(
            "/api/services",
            json={
                "service_name": "测试服务",
                "log_path": "./runtime_logs/missing",
                "source_type": "test",
                "enabled": True,
            },
        )
        assert response.status_code == 201
        services = client.get("/api/services").json()
        assert services["total"] >= 4
        assert client.delete(f"/api/services/{response.json()['id']}").status_code == 204


def test_service_path_must_stay_inside_allowed_root():
    with TestClient(app) as client:
        response = client.post(
            "/api/services",
            json={
                "service_name": "越界路径",
                "log_path": "../outside.log",
                "source_type": "test",
                "enabled": True,
            },
        )
        assert response.status_code == 400


def test_service_name_must_be_unique():
    payload = {
        "service_name": "唯一名称测试",
        "log_path": "./runtime_logs/missing",
        "source_type": "test",
        "enabled": True,
    }
    with TestClient(app) as client:
        first = client.post("/api/services", json=payload)
        assert first.status_code == 201
        duplicate = client.post("/api/services", json=payload)
        assert duplicate.status_code == 409
        assert client.delete(f"/api/services/{first.json()['id']}").status_code == 204


def test_log_query_and_statistics():
    with TestClient(app) as client:
        logs = client.get("/api/logs", params={"date":"2026-09-07","level":"ERROR"})
        assert logs.status_code == 200
        assert all(item["level"] == "ERROR" for item in logs.json()["items"])
        stats = client.get("/api/statistics/summary", params={"date":"2026-09-07"})
        assert stats.status_code == 200
        assert stats.json()["error_count"] >= 1
