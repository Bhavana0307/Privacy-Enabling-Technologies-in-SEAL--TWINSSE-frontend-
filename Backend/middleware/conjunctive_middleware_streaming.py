import os
import subprocess
import json
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(__file__)  # Folder where this script is located
DOCS_DIR = os.path.join(BASE_DIR, "docs")  # Your docs folder inside middleware
SETUP_BINARY = os.path.join(BASE_DIR, "../TWINSSE/conjunctive/sse_setup")
SEARCH_BINARY = os.path.join(BASE_DIR, "../TWINSSE/conjunctive/sse_search")
USER_QUERY_FILE = os.path.join(BASE_DIR, "user_query.txt")
RESULT_MAPPER_FILE = os.path.join(BASE_DIR, "result_mapper.json")
# ---------------------------

# Helper: Save doc ID → filename mapping
def save_result_mapping(mapping):
    with open(RESULT_MAPPER_FILE, "w") as f:
        json.dump(mapping, f)

# Helper: Load doc ID → filename mapping
def load_result_mapping():
    if os.path.exists(RESULT_MAPPER_FILE):
        with open(RESULT_MAPPER_FILE, "r") as f:
            return json.load(f)
    return {}

# ---------------- Setup ----------------
@app.route("/setup", methods=["POST"])
def setup_system():
    socketio.start_background_task(run_setup_steps)
    return jsonify({"status": "Setup started"}), 202

def run_setup_steps():
    steps = [
        "Generating Encrypted Documents...",
        "Generating Encrypted Search Index...",
        "Finalizing Setup..."
    ]
    for step in steps:
        socketio.emit("setup_status", {"message": step})
        time.sleep(1)  # Just for visible delay

    # Run setup binary
    try:
        subprocess.run([SETUP_BINARY, DOCS_DIR], check=True)
    except subprocess.CalledProcessError as e:
        socketio.emit("setup_status", {"message": f"Setup failed: {e}"})
        return

    # Create mapping from document IDs to filenames
    mapping = {str(i): fname for i, fname in enumerate(sorted(os.listdir(DOCS_DIR)), start=1)}
    save_result_mapping(mapping)

    socketio.emit("setup_status", {"message": "✅ Setup Completed Successfully"})

# ---------------- Search ----------------
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keywords = data.get("keywords", "")
    if not keywords.strip():
        return jsonify({"error": "No keywords provided"}), 400

    # Write keywords to file (backend reads file)
    with open(USER_QUERY_FILE, "w") as f:
        for kw in keywords.strip().split():
            f.write(kw + "\n")

    # Launch search in background
    socketio.start_background_task(run_search_stream, USER_QUERY_FILE)
    return jsonify({"status": "Search started"}), 202

def run_search_stream(query_file):
    mapping = load_result_mapping()
    try:
        process = subprocess.Popen(
            [SEARCH_BINARY, query_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            doc_id = line.strip()
            if doc_id in mapping:
                socketio.emit("search_result", {
                    "doc_id": doc_id,
                    "filename": mapping[doc_id]
                })

        process.wait()
        socketio.emit("search_complete", {"message": "Search finished"})

    except Exception as e:
        socketio.emit("search_error", {"message": str(e)})

# ---------------- Download ----------------
@app.route("/download/<doc_id>", methods=["GET"])
def download_file(doc_id):
    mapping = load_result_mapping()
    filename = mapping.get(doc_id)
    if not filename:
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(DOCS_DIR, filename, as_attachment=True)

# ---------------- Main ----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
