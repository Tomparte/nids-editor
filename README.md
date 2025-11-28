# NIDS Rules Editor

A lightweight Suricata/Snort rule builder that runs entirely in the browser with an optional Flask backend. It provides both a text editor and a structured table view so you can review, edit, and export `local.rules` without installing bulky tooling.

## Features
- Dual-pane experience: raw text editor with line numbers plus a sortable rules table.
- In-place editing modal with validation, duplicate-SID detection, and live previews.
- Quick filters to search rule messages, along with import/export helpers.
- Sample rules auto-load on first launch so newcomers can start modifying immediately.
- Optional Flask service that serves the UI, persists rules under `/rules/local.rules`, and restarts a Suricata container when changes are detected.

## Project Layout
```
.
├── docker-compose.yml      # Boots the Flask server and mounts rule/output volumes
├── rules-editor/
│   ├── app.py              # Minimal Flask app + file watcher
│   ├── Dockerfile          # Container definition for the editor service
│   └── index.html          # Single-page application (HTML/CSS/JS)
```
(Add a `suricata/rules/local.rules` file if you plan to mount real rule storage.)

## Quick Start
### 1. Browser-only mode
If you just want the UI with no backend integration, open `rules-editor/index.html` in any modern browser. All editing happens client-side, and you can import/export `.rules` files manually.

### 2. Docker Compose (with optional Suricata reloads)
1. Ensure Docker Desktop or Docker Engine is running.
2. (Optional) Create `suricata/rules/local.rules` so the container has a writable rules path.
3. From the repo root, run:
   ```bash
   docker compose up --build
   ```
4. Visit [http://localhost:8083](http://localhost:8083) to use the editor served by Flask (`app.py`).

When you POST rules to `/rules/local.rules` (e.g., by extending the UI or calling the API directly), `app.py` watches the file and restarts the Suricata container named in `SURICATA_CONTAINER` (defaults to `suricata`).

## Configuration
| Variable | Default | Description |
| --- | --- | --- |
| `RULES_FILE` | `/rules/local.rules` | Filesystem path where the Flask app reads/writes rules. |
| `SURICATA_CONTAINER` | `suricata` | Docker container name to restart after rule changes. |

Adjust these via `docker-compose.yml` or your deployment environment if your topology differs.

## Contributing
1. Fork the repo and create a feature branch.
2. Run the UI locally (browser or Docker) and ensure linting/formatting stay tidy.
3. Open a pull request describing the change, screenshots for UI tweaks, and any testing notes.

Issues, feature requests, and suggestions are always welcome. Enjoy building cleaner IDS rules!
