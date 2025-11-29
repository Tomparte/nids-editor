# NIDS Rules Editor

A lightweight Suricata/Snort rule builder that runs entirely in the browser. It provides both a text editor and a structured table view so you can review, edit, and export `local.rules` without installing bulky tooling.

## Features
- Dual-pane experience: raw text editor with line numbers plus a sortable rules table.
- In-place editing modal with validation, duplicate-SID detection, and live previews.
- Quick filters to search rule messages, along with import/export helpers.
- Sample rules auto-load on first launch so newcomers can start modifying immediately.
- Optional Docker container (Flask) that simply serves the static UI when you don't want to open the HTML file manually.

## Project Layout
```
.
├── docker-compose.yml      # Boots a minimal Flask server to host the SPA
├── rules-editor/
│   ├── app.py              # Static file server (Flask)
│   ├── Dockerfile          # Container definition for the editor service
│   └── index.html          # Single-page application (HTML/CSS/JS)
```

## Quick Start
### 1. Open in your browser
If you just want the UI, open `rules-editor/index.html` in any modern browser. All editing happens client-side, and you can import/export `.rules` files manually.

### 2. Docker Compose
1. Ensure Docker Desktop or Docker Engine is running.
2. From the repo root, run:
   ```bash
   docker compose up --build
   ```
3. Visit [http://localhost:8083](http://localhost:8083) to use the editor served by Flask (`rules-editor/app.py`).

No Suricata container or auto-save endpoint is bundled—the compose stack is only a convenient static host.

## Contributing
1. Fork the repo and create a feature branch.
2. Run the UI locally (browser or Docker) and ensure linting/formatting stay tidy.
3. Open a pull request describing the change, screenshots for UI tweaks, and any testing notes.

Issues, feature requests, and suggestions are always welcome. Enjoy building cleaner IDS rules!
