from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

# Paths
DOCS_DIR = "../TWINSSE/conjunctive/docs"
SETUP_BINARY = "../TWINSSE/conjunctive/sse_setup"
SEARCH_BINARY = "../TWINSSE/conjunctive/sse_search"
RESULT_MAPPER_FILE = "result_mapper.json"

# Load result mapping
if os.path.exists(RESULT_MAPPER_FILE):
    with open(RESULT_MAPPER_FILE, "r") as f:
        result_mapper = json.load(f)
else:
    result_mapper = {}

# ------------- /setup -------------
@app.route("/setup", methods=["POST"])
def setup():
    try:
        # Run the C++ setup binary
        subprocess.run([SETUP_BINARY], check=True)
        return jsonify({"status": "success", "message": "Setup complete!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Setup failed: {e}"})


# ------------- /search -------------
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keywords = data.get("keywords", [])

    if not keywords:
        return jsonify({"status": "error", "message": "No keywords provided."})

    # Prepare query string for backend
    query = " ".join(keywords)

    try:
        # Run the C++ search binary with input query
        result = subprocess.run([SEARCH_BINARY, query], capture_output=True, text=True, check=True)

        # Parse matched document IDs from output
        matched_ids = result.stdout.strip().split()
        readable_files = []

        for doc_id in matched_ids:
            filename = result_mapper.get(doc_id, f"{doc_id}.txt")
            if os.path.exists(os.path.join(DOCS_DIR, filename)):
                readable_files.append({"doc_id": doc_id, "filename": filename})

        if not readable_files:
            return jsonify({"status": "success", "matched_doc_ids": []})

        return jsonify({
            "status": "success",
            "matched_doc_ids": readable_files
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Search failed: {e}"})


# ------------- /download/<doc_id> -------------
@app.route("/download/<doc_id>", methods=["GET"])
def download(doc_id):
    filename = result_mapper.get(doc_id, f"{doc_id}.txt")
    try:
        return send_from_directory(DOCS_DIR, filename=filename, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"File not found: {e}"})


# ------------- Run the server -------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
