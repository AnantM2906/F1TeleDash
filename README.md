# F1 TeleDash

**Python · Flask · JavaScript · HTML/CSS · Chart.js**

A full-stack, responsive motorsport telemetry dashboard based on 

## Features
- Python telemetry simulator with reproducible lap, speed, sector, and tire-wear values.
- JSON API: `GET /api/telemetry?laps=18&seed=42`.
- Frontend with selectable driver and adjustable simulated lap count.
- Interactive speed, lap-time, sector split, and tire-wear charts.
- Computed standings and summary KPIs.
- Responsive layout, basic API validation, automated tests.

## Local setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. An internet connection is needed for the Chart.js CDN. No F1 credentials, data subscriptions, or external telemetry API required.

## Testing
```bash
pytest -q
```

## Architecture
`telemetry.py` (seeded simulator + ranking) → `app.py` (Flask API) → `static/dashboard.js` (fetch and chart updates) → `templates/index.html` and `static/style.css` (interface).

## Example response
`GET /api/telemetry?laps=1` returns a `source` field, a `records` array (one record per driver/lap), `standings`, and `drivers`.

## Next improvements
Replay slider, WebSocket live-stream simulation, pit-stop strategies, real permitted datasets, Docker deployment, and screenshot gallery. These are not implemented yet.

*No affiliation with Formula One Management or teams. Not official telemetry.*
