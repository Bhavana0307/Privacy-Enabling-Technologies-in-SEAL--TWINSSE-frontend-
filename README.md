# TWINSSE--frontend
The primary objective of this project is to implement Privacy Enabling Technologies using Searchable Symmetric Encryption (SSE). This project focuses on developing the frontend interface for encrypted search and a Python Flask middleware to communicate with a backend SSE engine (TWINSSE) for Conjunctive (AND) and Disjunctive (OR) keyword queries.

The implementation is inspired by the following research works:

*Highly Scalable Searchable Symmetric Encryption for Boolean Queries
Debadrita Talapatra, Indian Institute of Technology Kharagpur, Sikhar Patranabis, IBM Research India, and Debdeep Mukhopadhyay*
published in *IACR Communications in Cryptology (CIC)*, Volume 2, Number 2, 2025
DOI: [10.62056/ae89n59p1](https://cic.iacr.org/p/2/2/6).

TWINSSE Implementation Repository:
[TWINSSE](https://github.com/SEAL-IIT-KGP/TWINSSE) GitHub
provides the C++ backend implementation for encrypted search setup and query execution.

This project demonstrates how secure keyword search can be performed without exposing sensitive data, allowing developers and users to interact with encrypted datasets securely.

---

## System Requirements
- Python 3.8+
- Flask (pip install flask)
- Browser (for running the frontend)
- For system requirements and dependencies for backend , refer to [TWINSSE](https://github.com/SEAL-IIT-KGP/TWINSSE/blob/main/README.md) github repo.

---

## Repository Structure
```
NEW SSE WEBSITE
|-- Backend/
|   |-- build/                 # (placeholder for compiled C++ binaries)
|   |-- middleware/            # Flask middleware and utilities
|       |-- conjunctive_middleware.py         # Handles conjunctive (AND) search
|       |-- disjunctive_middleware.py         # Handles disjunctive (OR) search (dummy results for now)
|       |-- conjunctive_middleware_streaming.py # Alternate conjunctive handler with streaming
|       |-- file_server.py                    # Preview & download service for documents
|       |-- result_mapper.py                  # Generates human-readable doc mapping (JSON)
|       |-- result_mapper.json                # Auto-generated mapping (doc_id → readable filename)
|       |-- *.csv                             # Sample inverted index and keyword-docID maps
|       |-- docs/                             # Sample dataset (plaintext emails/files)
|
|-- Frontend/
|   |-- index.html              # Homepage
|   |-- encryptedsearch.html    # Entry page for encrypted search options
|   |-- conjunctive.html        # UI for AND-based queries
|   |-- disjunctive.html        # UI for OR-based queries
|   |-- styles/                 # CSS files
|   |   |-- style.css           # Main site styling
|   |   |-- search.css          # Search pages styling   
|
|-- TWINSSE/                     # External backend repository
|-- Dataset/                     # Sample dataset generation 
```
---

## Middleware Services

### Conjunctive Middleware (`conjunctive_middleware.py`)
- Integrates with **TWINSSE C++ backend**.  
- Handles **AND-based keyword search**.  
- Integration code is present, but **not yet tested**.  

### Disjunctive Middleware (`disjunctive_middleware.py`)
- Simulates **OR-based keyword search**.  
- Currently returns **dummy results** for testing purposes.  

### Result Mapper (`result_mapper.py`)
- Preprocesses dataset files.  
- Extracts **email subjects** and generates a JSON mapping (`result_mapper.json`)  
  from **document IDs → human-readable filenames**.  

### File Server (`file_server.py`)
Flask-based microservice for runtime document access:  
- `/files/<filename>` → Returns **JSON preview** (first 30 lines of the file).  
- `/download/<filename>` → Provides **complete file download**.  
- Enables the preview of the sample dataset used, in the frontend on the encryptedSearch page.  

---

## Frontend Interface

- `index.html` → Landing page with project overview.  
- `encryptedsearch.html` → Search selection (Conjunctive vs Disjunctive).  
- `conjunctive.html` → Search UI for AND queries (keyword input, results, downloads).  
- `disjunctive.html` → Search UI for OR queries (dummy integration).  
- `style.css` → General styles.  
- `search.css` → Search UI-specific animations and styling.  

---

## Dataset Preparation

- Test dataset created using **Enron Email dataset**.  
- Preprocessing pipeline generated:  
  - **Inverted Index CSV** (`inverted_index_test.csv`) → keyword → docID mapping.  
  - **Keyword-only CSV** (`keywords_only.csv`) → simplified list of searchable terms.  
  - **Keyword-DocName maps** for middleware lookup.  
- Used by middleware to simulate **encrypted search over emails**.  

---

## How to Run

1. Clone this repository along with the [TWINSSE](https://github.com/SEAL-IIT-KGP/TWINSSE).  

2. Install dependencies:
   ```bash
   pip install flask flask-cors

3. Generate document mappings (optional step):
   ```bash
   python middleware/result_mapper.py

4. Run middleware (example for conjunctive):
   ```bash
   python middleware/conjunctive_middleware.py
   ```
   (For disjunctive, run `disjunctive_middleware.py`)

5. Run file server for previews/downloads:
  ```bash
  python middleware/file_server.py
```

6. Open `Frontend/index.html` in your browser and interact with the search UI.

---

## Current Status

- Frontend contains home page and seperate pages for conjunctive search and disjunctive search.
- Middleware structured for both query types
- Preview + download feature implemented
- Conjunctive Middleware **integration code written but not tested with C++ backend**
- Disjunctive Middleware currently returns dummy results
- File server serves only from local middleware directory

---

## 
