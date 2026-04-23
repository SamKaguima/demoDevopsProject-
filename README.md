# DROVER Task Management System

A presentation-ready Flask demo app that simulates software delivery for the fictional DROVER engineering system and visualizes the 4 DORA metrics.

## DORA metrics covered

- Deployment Frequency
- Lead Time for Changes
- Change Failure Rate
- Mean Time to Recovery (MTTR)

## Features

- Dashboard with summary metric cards
- Recent deployments and incidents tables
- Plain-language DORA metric explanations
- Simulate failure action
- Recover system action
- Add successful deployment action
- Deployment history page
- Incident history page

## Tech stack

- Python + Flask
- Jinja HTML templates
- Simple CSS
- JSON files for local data storage
- Pytest tests
- GitHub Actions CI

## Project structure

- `app.py` – Flask routes and app setup
- `dora_utils.py` – metric calculation logic
- `data/deployments.json` – deployment records
- `data/incidents.json` – incident records
- `templates/` – dashboard and history pages
- `static/style.css` – UI styling
- `tests/` – route and metric tests
- `.github/workflows/ci.yml` – CI pipeline

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   flask --app app run --debug
   ```

4. Open `http://127.0.0.1:5000`

## Run tests

```bash
pytest -q
```
