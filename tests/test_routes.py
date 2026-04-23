import json
from pathlib import Path

import app as app_module


BASE_DIR = Path(__file__).resolve().parents[1]
DEPLOYMENTS = BASE_DIR / "data" / "deployments.json"
INCIDENTS = BASE_DIR / "data" / "incidents.json"


def _read(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write(path: Path, payload):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def test_dashboard_page_loads():
    client = app_module.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"DROVER Task Management System" in response.data


def test_simulate_failure_adds_records():
    original_deployments = _read(DEPLOYMENTS)
    original_incidents = _read(INCIDENTS)

    try:
        client = app_module.app.test_client()
        response = client.post("/simulate-failure", follow_redirects=False)
        assert response.status_code == 302

        new_deployments = _read(DEPLOYMENTS)
        new_incidents = _read(INCIDENTS)

        assert len(new_deployments) == len(original_deployments) + 1
        assert new_deployments[-1]["status"] == "failed"
        assert len(new_incidents) == len(original_incidents) + 1
        assert new_incidents[-1]["status"] == "active"
    finally:
        _write(DEPLOYMENTS, original_deployments)
        _write(INCIDENTS, original_incidents)


def test_recover_system_resolves_active_incident():
    original_incidents = _read(INCIDENTS)

    try:
        incidents = original_incidents + [
            {
                "id": 999,
                "deployment_id": 1,
                "start_timestamp": "2026-04-20T10:00:00+00:00",
                "resolved_timestamp": None,
                "duration_minutes": None,
                "severity": "high",
                "summary": "test active incident",
                "status": "active",
            }
        ]
        _write(INCIDENTS, incidents)

        client = app_module.app.test_client()
        response = client.post("/recover/", follow_redirects=False)
        assert response.status_code == 302

        updated = _read(INCIDENTS)
        latest = [i for i in updated if i["id"] == 999][0]
        assert latest["status"] == "resolved"
        assert latest["duration_minutes"] is not None
        assert latest["resolved_timestamp"] is not None
    finally:
        _write(INCIDENTS, original_incidents)
