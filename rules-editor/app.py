from flask import Flask, send_from_directory
from pathlib import Path

APP_ROOT = Path(__file__).parent.resolve()

app = Flask(
    __name__,
    static_folder=str(APP_ROOT),
    static_url_path=""
)


@app.route("/")
def root():
    """Serve the NIDS editor single-page app."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:asset>")
def assets(asset: str):
    """Serve other static assets that may be requested."""
    return send_from_directory(app.static_folder, asset)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
