# FruitAI Classifier (Local)

This project runs a local Hugging Face-compatible ResNet fruit model, with Flask backend, SQLite persistence, and a multi-page HTML UI.

## Run

1. Create and activate a Python 3.11 virtual environment.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open:

```text
http://127.0.0.1:5001
```

## Notes

- Prediction API: `POST /api/predict` with multipart field `image`.
- Health API: `GET /api/health`.
- Upload validation is strict on MIME, size (<10MB), and image parsing.
- Calories source: online lookup first (OpenFoodFacts), fallback map if online lookup fails.
- SQLite DB file: `fruitai.db` (auto-created).
- Uploaded images are stored in `uploads/` and listed in Admin page.

## Admin Login

- Email: `admin@gmail.com`
- Password: `admin123`

After login, admin gets checked image history from SQLite via `GET /api/admin/checked-images` with `X-Admin-Key`.
