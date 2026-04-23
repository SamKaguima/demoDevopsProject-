from dora_utils import calculate_metrics


def test_calculate_metrics_returns_expected_structure():
    deployments = [
        {
            "id": 1,
            "status": "success",
            "commit_timestamp": "2026-01-01T10:00:00+00:00",
            "deployment_timestamp": "2026-01-01T12:00:00+00:00",
        },
        {
            "id": 2,
            "status": "failed",
            "commit_timestamp": "2026-01-08T10:00:00+00:00",
            "deployment_timestamp": "2026-01-08T16:00:00+00:00",
        },
    ]
    incidents = [
        {
            "duration_minutes": 40,
            "status": "resolved",
        },
        {
            "duration_minutes": None,
            "status": "active",
        },
    ]

    metrics = calculate_metrics(deployments, incidents)

    assert metrics["total_deployments"] == 2
    assert metrics["successful_deployments"] == 1
    assert metrics["failed_deployments"] == 1
    assert metrics["change_failure_rate"] == 50.0
    assert metrics["avg_lead_time_hours"] == 4.0
    assert metrics["avg_mttr_minutes"] == 40
    assert metrics["deployment_frequency_per_week"] == 2.0
