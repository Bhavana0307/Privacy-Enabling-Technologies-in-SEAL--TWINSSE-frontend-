from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/files/<filename>', methods=['GET'])
def get_file_preview(filename):
    try:
        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            preview = ''.join(f.readlines()[:30])  # Preview: first 30 lines
        return jsonify({"filename": filename, "preview": preview})
    except Exception as e:
        return jsonify({"error": f"Could not read file: {str(e)}"}), 404

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Could not download file: {str(e)}"}), 404

if __name__ == '__main__':
    app.run(port=5050, debug=True)
