# DROVER Task Management System

Presentation-ready Flask demo app for teaching DORA metrics through a fictional software system (DROVER). The app simulates deployments and incidents, then computes and displays all four DORA metrics in a simple dashboard.

## Project overview

This project models a lightweight DevOps workflow:

- Deployments are stored in `data/deployments.json`
- Incidents are stored in `data/incidents.json`
- Metrics are calculated in `dora_utils.py`
- Flask routes in `app.py` drive simulation actions and pages

The dashboard lets you trigger realistic scenarios (successful release, failed release, recovery) and immediately see how the metrics change.

## Why this was built

This project was built as a classroom demo to make DORA metrics tangible.

- Instead of only defining metrics, students can interact with them
- Each button maps to a DevOps event and updates data in real time
- The app is intentionally small so the metric logic and CI pipeline are easy to explain

## Tech stack

- Python + Flask
- Jinja HTML templates
- CSS
- JSON files for local data
- Pytest
- GitHub Actions

## Project structure

- `app.py`: Flask app, routes, and simulation actions
- `dora_utils.py`: DORA metric calculations
- `data/deployments.json`: deployment history data
- `data/incidents.json`: incident history data
- `templates/`: dashboard and history page templates
- `static/style.css`: UI styling
- `tests/`: route and metric tests
- `.github/workflows/ci.yml`: CI workflow definition

## Install and run locally

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate it:

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   flask --app app run --debug
   ```

5. Open the dashboard:

   ```
   http://127.0.0.1:5000
   ```

## Run tests locally

```bash
pytest -q
```

## GitHub Actions CI pipeline

The CI workflow is defined in `.github/workflows/ci.yml` and runs on:

- every push to any branch
- every pull request

Pipeline steps:

1. Checkout repository code
2. Set up Python 3.11
3. Upgrade pip and install dependencies from `requirements.txt`
4. Run `pytest -q`

If tests fail, the workflow fails, which prevents merging broken changes with branch protection enabled.

## How each DORA metric is demonstrated

The dashboard computes metrics from the JSON datasets after every action.

1. Deployment Frequency
   Demonstrated by adding deployments over time (especially with Add Successful Deployment). More deployments in the measured period increase deployments/week.

2. Lead Time for Changes
   Demonstrated using commit timestamp to deployment timestamp per deployment. The app averages these durations (in hours).

3. Change Failure Rate
   Demonstrated when a deployment has `status: failed`. Simulate Failure increases the failed count and therefore failure rate.

4. Mean Time to Recovery (MTTR)
   Demonstrated by resolving active incidents. Recover System sets resolution time and duration; MTTR is the average duration of resolved incidents.

## Simulate a failed deployment

From the dashboard:

1. Click Simulate Failure
2. The app creates:
   - a failed deployment record
   - a new active high-severity incident linked to that deployment
3. You will see:
   - Change Failure Rate increase
   - an active incident appear in recent incident data

## Recover from an incident

From the dashboard:

1. Click Recover System
2. The app finds the most recent active incident
3. It marks the incident as resolved and computes duration in minutes
4. You will see:
   - active incident count drop
   - MTTR update based on resolved incident durations

## Short presentation script (example talking points)

Use this 2-3 minute script as a class demo guide:

1. "This is a Flask app that simulates a software delivery system and visualizes all four DORA metrics."
2. "Deployments and incidents are stored as simple JSON so we can focus on metric behavior, not infrastructure complexity."
3. "I will click Add Successful Deployment to show how Deployment Frequency changes as releases increase."
4. "Lead Time for Changes is computed from commit time to deployment time and shown as an average in hours."
5. "Now I click Simulate Failure, which creates a failed deployment and an active incident. Notice Change Failure Rate increases."
6. "Finally, I click Recover System. That resolves the incident and records duration, which feeds Mean Time to Recovery."
7. "This demo shows how engineering actions immediately affect delivery performance indicators and why balanced DevOps practices matter."
