# Changelog

| Version | Date       | Description                                                        |
|---------|------------|--------------------------------------------------------------------|
| 1.2     | 2026-10-27 | Skip NYT's new "Continue to Wordle" ad interstitial and fix the cookie "Reject all" selector, which together left the board unrendered and caused empty games since 2026-09-21. Docker deployment now bind-mounts `results.csv` so results survive rebuilds. Backfill 117 missed or empty days (2026-05-01 to 2026-10-24) with simulated games. |
| 1.1     | 2026-04-30 | Fix Chrome crash in Docker (--headless=new, --disable-gpu, --remote-debugging-port=0), fix tile animation timing with retry polling, dismiss overlay dialogs before guessing, prevent duplicate guess loop, add crash recovery. Backfill Apr 24-29. |
| 1.0     | 2026-04-23 | Major restructure: deployment-ready repo with bug fixes, Docker support, and clean file layout |
