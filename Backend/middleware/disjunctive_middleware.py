from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv

app = Flask(__name__)
CORS(app)

# Correct path to the keyword-docID CSV and documents directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYWORD_DOCID_CSV = os.path.join(BASE_DIR, "keyword_docid_map.csv")
DOCUMENT_DIR = os.path.join(BASE_DIR, "docs")

# In-memory map of keyword → set of document IDs
keyword_docid_map = {}

# ------------------ SETUP ------------------
@app.route('/setup', methods=['POST'])
def setup():
    global keyword_docid_map
    keyword_docid_map = {}

    try:
        with open(KEYWORD_DOCID_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) >= 2:
                    keyword = row[0].strip().lower()
                    doc_ids = [doc_id.strip() for doc_id in row[1].split(",") if doc_id.strip()]
                    if keyword not in keyword_docid_map:
                        keyword_docid_map[keyword] = set()
                    keyword_docid_map[keyword].update(doc_ids)
        return jsonify({"status": "success", "message": "Setup complete for Disjunctive Search."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ------------------ SEARCH (OR-based) ------------------
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keywords = data.get("keywords", [])

    if not keywords or not keyword_docid_map:
        return jsonify({"status": "error", "message": "Missing keywords or setup not done."})

    matching_docs = set()
    for keyword in keywords:
        keyword = keyword.lower()
        matching_docs.update(keyword_docid_map.get(keyword, set()))

    return jsonify({
        "status": "success",
        "matched_doc_ids": sorted(matching_docs)
    })

# ------------------ DOWNLOAD ------------------
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(DOCUMENT_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"File not found: {str(e)}"})

# ------------------ MAIN ------------------
if __name__ == '__main__':
    if not os.path.exists(DOCUMENT_DIR):
        os.makedirs(DOCUMENT_DIR)
    app.run(debug=True, port=5001)
