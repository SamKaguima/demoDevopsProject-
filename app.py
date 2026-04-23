from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, redirect, render_template, url_for

from dora_utils import calculate_metrics

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DEPLOYMENTS_FILE = DATA_DIR / "deployments.json"
INCIDENTS_FILE = DATA_DIR / "incidents.json"


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def dashboard() -> str:
        deployments = load_json(DEPLOYMENTS_FILE)
        incidents = load_json(INCIDENTS_FILE)
        metrics = calculate_metrics(deployments, incidents)

        recent_deployments = sorted(
            deployments, key=lambda d: d["deployment_timestamp"], reverse=True
        )[:6]
        recent_incidents = sorted(
            incidents, key=lambda i: i["start_timestamp"], reverse=True
        )[:6]

        active_incidents = [incident for incident in incidents if incident["status"] == "active"]

        return render_template(
            "dashboard.html",
            metrics=metrics,
            recent_deployments=recent_deployments,
            recent_incidents=recent_incidents,
            active_incidents=active_incidents,
        )

    @app.route("/deployments")
    def deployments_page() -> str:
        deployments = load_json(DEPLOYMENTS_FILE)
        deployments_sorted = sorted(
            deployments, key=lambda d: d["deployment_timestamp"], reverse=True
        )
        return render_template("deployments.html", deployments=deployments_sorted)

    @app.route("/incidents")
    def incidents_page() -> str:
        incidents = load_json(INCIDENTS_FILE)
        incidents_sorted = sorted(incidents, key=lambda i: i["start_timestamp"], reverse=True)
        return render_template("incidents.html", incidents=incidents_sorted)

    @app.post("/simulate-failure")
    def simulate_failure():
        deployments = load_json(DEPLOYMENTS_FILE)
        incidents = load_json(INCIDENTS_FILE)

        deployment_id = max(d["id"] for d in deployments) + 1
        incident_id = max(i["id"] for i in incidents) + 1 if incidents else 1
        timestamp = now_iso()

        deployments.append(
            {
                "id": deployment_id,
                "version": f"v1.{deployment_id}.0",
                "commit_id": f"sim{deployment_id:04d}",
                "commit_timestamp": timestamp,
                "deployment_timestamp": timestamp,
                "status": "failed",
                "environment": "production",
                "developer": "Simulation Bot",
                "notes": "Simulated failed deployment for presentation.",
            }
        )

        incidents.append(
            {
                "id": incident_id,
                "deployment_id": deployment_id,
                "start_timestamp": timestamp,
                "resolved_timestamp": None,
                "duration_minutes": None,
                "severity": "high",
                "summary": "Simulated service disruption after failed release.",
                "status": "active",
            }
        )

        save_json(DEPLOYMENTS_FILE, deployments)
        save_json(INCIDENTS_FILE, incidents)
        return redirect(url_for("dashboard"))

    @app.post("/recover/")
    def recover_system():
        incidents = load_json(INCIDENTS_FILE)
        active_incidents = [incident for incident in incidents if incident["status"] == "active"]

        if active_incidents:
            latest = sorted(active_incidents, key=lambda i: i["start_timestamp"], reverse=True)[0]
            started = datetime.fromisoformat(latest["start_timestamp"])
            resolved = datetime.now(timezone.utc).replace(microsecond=0)
            duration_minutes = max(int((resolved - started).total_seconds() // 60), 1)

            latest["resolved_timestamp"] = resolved.isoformat()
            latest["duration_minutes"] = duration_minutes
            latest["status"] = "resolved"

        save_json(INCIDENTS_FILE, incidents)
        return redirect(url_for("dashboard"))

    @app.post("/add-successful-deployment")
    def add_successful_deployment():
        deployments = load_json(DEPLOYMENTS_FILE)
        deployment_id = max(d["id"] for d in deployments) + 1

        deploy_time = datetime.now(timezone.utc).replace(microsecond=0)
        commit_time = deploy_time.replace(hour=max(deploy_time.hour - 6, 0))

        deployments.append(
            {
                "id": deployment_id,
                "version": f"v1.{deployment_id}.0",
                "commit_id": f"succ{deployment_id:04d}",
                "commit_timestamp": commit_time.isoformat(),
                "deployment_timestamp": deploy_time.isoformat(),
                "status": "success",
                "environment": "production",
                "developer": "Release Bot",
                "notes": "Simulated successful deployment for presentation.",
            }
        )

        save_json(DEPLOYMENTS_FILE, deployments)
        return redirect(url_for("dashboard"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
