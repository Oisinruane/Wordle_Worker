# Changelog

| Version | Date       | Description                                                        |
|---------|------------|--------------------------------------------------------------------|
| 1.4     | 2026-10-29 | Web page ready for public access: today's result is blurred behind a "Click to reveal" button to avoid spoilers; guess distribution shows counts above the bars and empty buckets as grey, so 0 no longer looks like a win and small counts are readable. Deployment now includes the `/api/results` endpoint. |
| 1.3     | 2026-10-29 | Fix duplicate-letter handling in the solver: a grey copy of a letter that is green or yellow elsewhere no longer rules the letter out entirely (lost GEEKY on 2026-10-26). The solver now tracks minimum/maximum letter counts and excluded positions. Add `tests/test_solver.py`. Past results are unchanged. |
| 1.2     | 2026-10-27 | Skip NYT's new "Continue to Wordle" ad interstitial and fix the cookie "Reject all" selector, which together left the board unrendered and caused empty games since 2026-09-21. Docker deployment now bind-mounts `results.csv` so results survive rebuilds. Backfill 117 missed or empty days (2026-05-01 to 2026-10-24) with simulated games. |
| 1.1     | 2026-04-30 | Fix Chrome crash in Docker (--headless=new, --disable-gpu, --remote-debugging-port=0), fix tile animation timing with retry polling, dismiss overlay dialogs before guessing, prevent duplicate guess loop, add crash recovery. Backfill Apr 24-29. |
| 1.0     | 2026-04-23 | Major restructure: deployment-ready repo with bug fixes, Docker support, and clean file layout |
