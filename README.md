# Wordle Worker

An automated Wordle solver that plays the daily NYT Wordle puzzle using Selenium and serves results via a Flask web dashboard.

## Architecture

- **Play_Script.py** — Selenium-based solver. Opens Wordle in headless Chrome, plays using a scored word list, and logs results to `results.csv`.
- **WebServer.py** — Flask app (served via Waitress on port 5001) that reads `results.csv` and renders a dashboard with today's attempt, history, and guess distribution.
- **main.py** — Entrypoint. Runs the web server in a thread and schedules the solver to run daily at 01:00 UTC.
- **word_scores.csv** — Pre-scored word list used to rank guesses.
- **word_scorer.py** — Utility to regenerate `word_scores.csv` from a raw word list.

## Docker Deployment

```bash
docker build -t wordle-worker .
docker run -d -p 5001:5001 --name wordle-worker wordle-worker
```

The dashboard is available at `http://<host>:5001`.

## Local Development

```bash
pip install -r requirements.txt
python main.py
```
