from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any


def _parse(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)


def calculate_metrics(
    deployments: list[dict[str, Any]], incidents: list[dict[str, Any]]
) -> dict[str, float | int]:
    total_deployments = len(deployments)
    successful_deployments = sum(1 for deployment in deployments if deployment["status"] == "success")
    failed_deployments = total_deployments - successful_deployments

    deployment_frequency_per_week = 0.0
    if total_deployments > 0:
        ordered = sorted(deployments, key=lambda d: d["deployment_timestamp"])
        first = _parse(ordered[0]["deployment_timestamp"])
        last = _parse(ordered[-1]["deployment_timestamp"])
        days = max((last - first).days, 1)
        weeks = max(days / 7, 1)
        deployment_frequency_per_week = total_deployments / weeks

    lead_times_hours: list[float] = []
    for deployment in deployments:
        commit_time = _parse(deployment["commit_timestamp"])
        deployment_time = _parse(deployment["deployment_timestamp"])
        lead_times_hours.append(max((deployment_time - commit_time).total_seconds() / 3600, 0))

    avg_lead_time_hours = mean(lead_times_hours) if lead_times_hours else 0.0

    change_failure_rate = (
        (failed_deployments / total_deployments) * 100 if total_deployments else 0.0
    )

    resolved_durations = [
        incident["duration_minutes"]
        for incident in incidents
        if incident.get("duration_minutes") is not None and incident.get("status") == "resolved"
    ]
    avg_mttr_minutes = mean(resolved_durations) if resolved_durations else 0.0

    return {
        "total_deployments": total_deployments,
        "successful_deployments": successful_deployments,
        "failed_deployments": failed_deployments,
        "deployment_frequency_per_week": round(deployment_frequency_per_week, 2),
        "avg_lead_time_hours": round(avg_lead_time_hours, 2),
        "change_failure_rate": round(change_failure_rate, 2),
        "avg_mttr_minutes": round(avg_mttr_minutes, 2),
    }
