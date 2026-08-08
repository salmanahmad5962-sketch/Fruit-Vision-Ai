import io
import json
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, request, send_from_directory
from authlib.integrations.flask_client import OAuth
from PIL import Image
import numpy as np
import torch
from transformers import AutoModelForImageClassification
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# ── Health Info: Health Benefits / Helpful For / Vitamins / Warnings ──
from fruit_health_info import get_health_info
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, HRFlowable
)
# ═══════════════════════════════════════════════
# APP SETUP
# ═══════════════════════════════════════════════
app = Flask(
    __name__,
    static_folder=os.path.dirname(os.path.abspath(__file__)),
    static_url_path="",
)
app.config['SECRET_KEY']         = os.getenv("SECRET_KEY", "dev-only-change-me")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

oauth  = OAuth(app)
google = oauth.register(
    name='google',
    client_id     = os.getenv("GOOGLE_CLIENT_ID", ""),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", ""),
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope': 'openid email profile'},
)

# ═══════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════
MODEL_PATH     = os.path.join(os.path.dirname(__file__), "models")
DB_PATH        = os.path.join(os.path.dirname(__file__), "fruitai.db")
UPLOAD_DIR     = os.path.join(os.path.dirname(__file__), "uploads")
ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ALLOWED_IMAGE_MIME = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

# ── FIX 1: Known fruit/vegetable allowlist ──────
KNOWN_FRUIT_LABELS = {
    "apple", "banana", "grapes", "grape", "watermelon", "orange", "mango",
    "strawberry", "pineapple", "kiwi", "lemon", "pear", "peach", "cherry",
    "pomegranate", "papaya", "guava", "blueberry", "raspberry", "coconut",
    "fig", "plum", "apricot", "avocado", "tomato", "cucumber", "carrot",
    "potato", "onion", "garlic", "corn", "capsicum", "bell pepper",
    "cabbage", "cauliflower", "eggplant", "beetroot", "ginger", "melon",
    "dragonfruit", "passion fruit", "lychee", "jackfruit", "mulberry",
    "gooseberry", "cranberry", "mandarin", "tangerine", "lime", "nectarine",
    "date", "olive", "pepper", "zucchini", "broccoli", "spinach", "lettuce",
    "celery", "mushroom", "radish", "turnip", "yam", "sweet potato",
    "pumpkin", "squash", "asparagus", "artichoke", "leek",
}
# ── FIX 1: Reject if confidence below this ──────
CONFIDENCE_THRESHOLD = 0.40

STRAWBERRY_FALLBACK_ENABLED       = os.getenv("STRAWBERRY_FALLBACK_ENABLED", "1") == "1"
STRAWBERRY_MODEL_ID               = os.getenv("STRAWBERRY_MODEL_ID", "dima806/fruit_100_types_image_detection")
STRAWBERRY_RED_RATIO              = float(os.getenv("STRAWBERRY_RED_RATIO", "0.18"))
STRAWBERRY_PRIMARY_MAX_CONFIDENCE = float(os.getenv("STRAWBERRY_PRIMARY_MAX_CONFIDENCE", "0.55"))
STRAWBERRY_SCORE_THRESHOLD        = float(os.getenv("STRAWBERRY_SCORE_THRESHOLD", "0.2"))

# ═══════════════════════════════════════════════
# LOAD AI MODEL
# ═══════════════════════════════════════════════
print("System: Loading ResNet-50 model...")
processor_config = {
    "size": 224,
    "image_mean": [0.485, 0.456, 0.406],
    "image_std":  [0.229, 0.224, 0.225],
}

try:
    config_path = os.path.join(MODEL_PATH, "preprocessor_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as fp:
            loaded_config = json.load(fp)
            if isinstance(loaded_config.get("size"), dict):
                processor_config["size"] = int(loaded_config["size"].get("shortest_edge", 224))
            else:
                processor_config["size"] = int(loaded_config.get("size", 224))
            processor_config["image_mean"] = loaded_config.get("image_mean", processor_config["image_mean"])
            processor_config["image_std"]  = loaded_config.get("image_std",  processor_config["image_std"])

    model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)
    model.eval()
    print("System: Model loaded! Ready for predictions.")
except Exception as e:
    print(f"System Error: Could not load model. {e}")
    model = None

strawberry_model            = None
strawberry_processor_config = None
strawberry_model_ready      = False
strawberry_model_lock       = threading.Lock()

# ═══════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════
def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with db_connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS admin_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY(admin_id) REFERENCES admin_users(id))""")
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        conn.execute("""CREATE TABLE IF NOT EXISTS checked_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            fruit_label TEXT NOT NULL,
            confidence REAL NOT NULL,
            calories_per_100g INTEGER NOT NULL,
            calories_source TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        try:
            conn.execute("ALTER TABLE checked_images ADD COLUMN user_id INTEGER REFERENCES users(id)")
        except Exception:
            pass
        conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        conn.execute(
            "INSERT OR IGNORE INTO admin_users (email, password_hash) VALUES (?, ?)",
            (ADMIN_EMAIL, generate_password_hash(ADMIN_PASSWORD)),
        )
    print("Database ready!")

# ═══════════════════════════════════════════════
# AUTH HELPERS
# ═══════════════════════════════════════════════
def require_admin_token():
    token = request.headers.get("X-Admin-Key", "").strip()
    if not token:
        return None
    now_iso = datetime.now(timezone.utc).isoformat()
    with db_connect() as conn:
        return conn.execute(
            "SELECT u.id, u.email FROM admin_sessions s "
            "INNER JOIN admin_users u ON u.id = s.admin_id "
            "WHERE s.token = ? AND s.expires_at > ?",
            (token, now_iso),
        ).fetchone()

def require_user_token():
    token = request.headers.get("X-User-Token", "").strip()
    if not token:
        return None
    now_iso = datetime.now(timezone.utc).isoformat()
    with db_connect() as conn:
        return conn.execute(
            "SELECT u.id, u.username, u.email FROM user_sessions s "
            "INNER JOIN users u ON u.id = s.user_id "
            "WHERE s.token = ? AND s.expires_at > ?",
            (token, now_iso),
        ).fetchone()

# ═══════════════════════════════════════════════
# NUTRITION — LOCAL ONLY (FIX 2: no network calls)
# ═══════════════════════════════════════════════
NUTRIENTS_DB = {
    "apple":       {"calories": 52,  "carbohydrates": 14.0, "fat": 0.2, "protein": 0.3, "fiber": 2.4, "sugar": 10.0},
    "banana":      {"calories": 89,  "carbohydrates": 23.0, "fat": 0.3, "protein": 1.1, "fiber": 2.6, "sugar": 12.0},
    "beetroot":    {"calories": 43,  "carbohydrates": 10.0, "fat": 0.2, "protein": 1.6, "fiber": 2.8, "sugar": 7.0},
    "bell pepper": {"calories": 20,  "carbohydrates": 4.6,  "fat": 0.2, "protein": 0.9, "fiber": 1.7, "sugar": 2.4},
    "cabbage":     {"calories": 25,  "carbohydrates": 5.8,  "fat": 0.1, "protein": 1.3, "fiber": 2.5, "sugar": 3.2},
    "capsicum":    {"calories": 20,  "carbohydrates": 4.6,  "fat": 0.2, "protein": 0.9, "fiber": 1.7, "sugar": 2.4},
    "carrot":      {"calories": 41,  "carbohydrates": 9.6,  "fat": 0.2, "protein": 0.9, "fiber": 2.8, "sugar": 4.7},
    "cauliflower": {"calories": 25,  "carbohydrates": 5.0,  "fat": 0.3, "protein": 1.9, "fiber": 2.0, "sugar": 1.9},
    "corn":        {"calories": 86,  "carbohydrates": 19.0, "fat": 1.2, "protein": 3.2, "fiber": 2.7, "sugar": 3.2},
    "cucumber":    {"calories": 15,  "carbohydrates": 3.6,  "fat": 0.1, "protein": 0.7, "fiber": 0.5, "sugar": 1.7},
    "eggplant":    {"calories": 25,  "carbohydrates": 6.0,  "fat": 0.2, "protein": 1.0, "fiber": 3.0, "sugar": 3.5},
    "garlic":      {"calories": 149, "carbohydrates": 33.0, "fat": 0.5, "protein": 6.4, "fiber": 2.1, "sugar": 1.0},
    "ginger":      {"calories": 80,  "carbohydrates": 18.0, "fat": 0.8, "protein": 1.8, "fiber": 2.0, "sugar": 1.7},
    "grapes":      {"calories": 69,  "carbohydrates": 18.0, "fat": 0.2, "protein": 0.7, "fiber": 0.9, "sugar": 15.0},
    "kiwi":        {"calories": 61,  "carbohydrates": 15.0, "fat": 0.5, "protein": 1.1, "fiber": 3.0, "sugar": 9.0},
    "lemon":       {"calories": 29,  "carbohydrates": 9.0,  "fat": 0.3, "protein": 1.1, "fiber": 2.8, "sugar": 2.5},
    "mango":       {"calories": 60,  "carbohydrates": 15.0, "fat": 0.4, "protein": 0.8, "fiber": 1.6, "sugar": 14.0},
    "onion":       {"calories": 40,  "carbohydrates": 9.0,  "fat": 0.1, "protein": 1.1, "fiber": 1.7, "sugar": 4.2},
    "orange":      {"calories": 47,  "carbohydrates": 12.0, "fat": 0.1, "protein": 0.9, "fiber": 2.4, "sugar": 9.0},
    "pear":        {"calories": 57,  "carbohydrates": 15.0, "fat": 0.1, "protein": 0.4, "fiber": 3.1, "sugar": 10.0},
    "pineapple":   {"calories": 50,  "carbohydrates": 13.0, "fat": 0.1, "protein": 0.5, "fiber": 1.4, "sugar": 10.0},
    "pomegranate": {"calories": 83,  "carbohydrates": 19.0, "fat": 1.2, "protein": 1.7, "fiber": 4.0, "sugar": 13.7},
    "potato":      {"calories": 77,  "carbohydrates": 17.0, "fat": 0.1, "protein": 2.0, "fiber": 2.2, "sugar": 0.8},
    "strawberry":  {"calories": 32,  "carbohydrates": 7.7,  "fat": 0.3, "protein": 0.7, "fiber": 2.0, "sugar": 4.9},
    "tomato":      {"calories": 18,  "carbohydrates": 3.9,  "fat": 0.2, "protein": 0.9, "fiber": 1.2, "sugar": 2.6},
    "watermelon":  {"calories": 30,  "carbohydrates": 8.0,  "fat": 0.2, "protein": 0.6, "fiber": 0.4, "sugar": 6.2},
    "peach":       {"calories": 39,  "carbohydrates": 10.0, "fat": 0.3, "protein": 0.9, "fiber": 1.5, "sugar": 8.4},
    "cherry":      {"calories": 50,  "carbohydrates": 12.0, "fat": 0.3, "protein": 1.0, "fiber": 1.6, "sugar": 8.0},
    "plum":        {"calories": 46,  "carbohydrates": 11.0, "fat": 0.3, "protein": 0.7, "fiber": 1.4, "sugar": 9.9},
    "coconut":     {"calories": 354, "carbohydrates": 15.0, "fat": 33.0,"protein": 3.3, "fiber": 9.0, "sugar": 6.2},
    "lime":        {"calories": 30,  "carbohydrates": 11.0, "fat": 0.2, "protein": 0.7, "fiber": 2.8, "sugar": 1.7},
    "avocado":     {"calories": 160, "carbohydrates": 9.0,  "fat": 15.0,"protein": 2.0, "fiber": 7.0, "sugar": 0.7},
    "pumpkin":     {"calories": 26,  "carbohydrates": 7.0,  "fat": 0.1, "protein": 1.0, "fiber": 0.5, "sugar": 2.8},
    "broccoli":    {"calories": 34,  "carbohydrates": 7.0,  "fat": 0.4, "protein": 2.8, "fiber": 2.6, "sugar": 1.7},
}

def resolve_nutrients(label: str) -> tuple[dict, str]:
    """Fast local lookup — zero network calls."""
    lower = label.lower().replace("_", " ")
    for key, value in NUTRIENTS_DB.items():
        if key in lower:
            return value, "local"
    return {"calories": 50, "carbohydrates": 10.0, "fat": 0.2,
            "protein": 1.0, "fiber": 2.0, "sugar": 8.0}, "local"

# ═══════════════════════════════════════════════
# IMAGE PROCESSING
# ═══════════════════════════════════════════════
def preprocess_image(img: Image.Image) -> dict:
    size = int(processor_config.get("size", 224))
    mean = np.array(processor_config.get("image_mean", [0.485, 0.456, 0.406]), dtype=np.float32)
    std  = np.array(processor_config.get("image_std",  [0.229, 0.224, 0.225]), dtype=np.float32)
    img  = img.resize((size, size), Image.BILINEAR)
    arr  = np.asarray(img, dtype=np.float32) / 255.0
    arr  = (arr - mean) / std
    arr  = np.transpose(arr, (2, 0, 1))
    return {"pixel_values": torch.from_numpy(arr).unsqueeze(0)}

def red_pixel_ratio(img: Image.Image) -> float:
    thumb = img.resize((64, 64))
    arr   = np.asarray(thumb, dtype=np.float32)
    if arr.ndim != 3 or arr.shape[2] < 3:
        return 0.0
    r, g, b  = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    red_mask = (r > 150) & (r > g * 1.2) & (r > b * 1.2)
    return float(np.mean(red_mask))

def load_strawberry_model():
    global strawberry_model, strawberry_processor_config, strawberry_model_ready
    if not STRAWBERRY_FALLBACK_ENABLED:
        return None, processor_config
    if strawberry_model_ready:
        return strawberry_model, strawberry_processor_config or processor_config
    with strawberry_model_lock:
        if strawberry_model_ready:
            return strawberry_model, strawberry_processor_config or processor_config
        try:
            strawberry_model = AutoModelForImageClassification.from_pretrained(STRAWBERRY_MODEL_ID)
            strawberry_model.eval()
        except Exception as e:
            print(f"Strawberry model unavailable: {e}")
            strawberry_model = None
        strawberry_model_ready = True
        return strawberry_model, strawberry_processor_config or processor_config

def maybe_override_strawberry(img: Image.Image, label: str, confidence: float) -> tuple[str, float]:
    if not STRAWBERRY_FALLBACK_ENABLED:                 return label, confidence
    if "strawberry" in label.lower():                   return label, confidence
    if confidence >= STRAWBERRY_PRIMARY_MAX_CONFIDENCE: return label, confidence
    if red_pixel_ratio(img) < STRAWBERRY_RED_RATIO:    return label, confidence
    model_fb, config = load_strawberry_model()
    if model_fb is None:                                return label, confidence
    size = int(config.get("size", 224))
    mean = np.array(config.get("image_mean", [0.485, 0.456, 0.406]), dtype=np.float32)
    std  = np.array(config.get("image_std",  [0.229, 0.224, 0.225]), dtype=np.float32)
    tmp  = img.resize((size, size), Image.BILINEAR)
    arr  = (np.asarray(tmp, dtype=np.float32) / 255.0 - mean) / std
    arr  = np.transpose(arr, (2, 0, 1))
    inp  = {"pixel_values": torch.from_numpy(arr).unsqueeze(0)}
    with torch.inference_mode():
        logits = model_fb(**inp).logits
    probs = torch.nn.functional.softmax(logits, dim=1)[0]
    topk  = torch.topk(probs, k=3)
    top_labels = [model_fb.config.id2label.get(int(i), "") for i in topk.indices.tolist()]
    sb_score   = sum(float(probs[i]) for i in range(len(probs))
                     if "strawberry" in model_fb.config.id2label.get(int(i), "").lower())
    if any("strawberry" in n.lower() for n in top_labels) and sb_score >= STRAWBERRY_SCORE_THRESHOLD:
        return "strawberry", sb_score
    return label, confidence

def save_uploaded_image(image_bytes: bytes, original_name: str) -> tuple[str, str]:
    safe_name   = secure_filename(original_name or "upload.png") or "upload.png"
    stamp       = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    stored_name = f"{stamp}_{safe_name}"
    with open(os.path.join(UPLOAD_DIR, stored_name), "wb") as fp:
        fp.write(image_bytes)
    return stored_name, f"/uploads/{stored_name}"

def record_checked_image(image_name, image_path, label, confidence, calories, cal_source, user_id=None):
    with db_connect() as conn:
        conn.execute(
            "INSERT INTO checked_images (user_id, image_name, image_path, fruit_label, "
            "confidence, calories_per_100g, calories_source, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (user_id, image_name, image_path, label, confidence,
             calories, cal_source, datetime.now(timezone.utc).isoformat()),
        )
# ═══════════════════════════════════════════════
# PDF REPORT GENERATION
# ═══════════════════════════════════════════════
def build_pdf_report(data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"],
        fontSize=22, textColor=colors.HexColor("#00a085"), spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#636e72"), spaceAfter=14,
    )
    section_style = ParagraphStyle(
        "SectionStyle", parent=styles["Heading2"],
        fontSize=13, textColor=colors.HexColor("#2d3436"),
        spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["Normal"], fontSize=10, leading=15,
    )
    bullet_style = ParagraphStyle(
        "BulletStyle", parent=styles["Normal"], fontSize=10, leading=15,
        leftIndent=14, bulletIndent=2,
    )

    story = []

    # ── Header ──
    story.append(Paragraph("FruitAI — Nutrition &amp; Health Report", title_style))
    generated_at = datetime.now(timezone.utc).strftime("%d %B %Y, %I:%M %p UTC")
    story.append(Paragraph(f"Generated on {generated_at}", subtitle_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#e0e0e0"), thickness=1))
    story.append(Spacer(1, 12))

    # ── Fruit image (if it exists on disk) ──
    image_url = data.get("image_url", "")
    if image_url:
        img_path = os.path.join(UPLOAD_DIR, os.path.basename(image_url))
        if os.path.exists(img_path):
            try:
                story.append(RLImage(img_path, width=2.2 * inch, height=2.2 * inch))
                story.append(Spacer(1, 10))
            except Exception:
                pass

    # ── Fruit name + confidence ──
    fruit_name = data.get("fruit_name", "Unknown")
    confidence = float(data.get("confidence", 0)) * 100
    story.append(Paragraph(f"<b>Detected:</b> {fruit_name}", body_style))
    story.append(Paragraph(f"<b>Confidence:</b> {confidence:.2f}%", body_style))
    story.append(Spacer(1, 6))

    # ── Nutrition table ──
    story.append(Paragraph("Nutritional Information (per 100g)", section_style))
    nutrients = data.get("nutrients", {}) or {}
    nutrient_rows = [
        ["Calories", f'{nutrients.get("calories", data.get("calories_per_100g", 0))} kcal'],
        ["Carbohydrates", f'{nutrients.get("carbohydrates", 0)} g'],
        ["Fat", f'{nutrients.get("fat", 0)} g'],
        ["Protein", f'{nutrients.get("protein", 0)} g'],
        ["Fiber", f'{nutrients.get("fiber", 0)} g'],
        ["Sugar", f'{nutrients.get("sugar", 0)} g'],
    ]
    nutrient_table = Table([["Nutrient", "Amount"]] + nutrient_rows, colWidths=[3 * inch, 2.5 * inch])
    nutrient_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00b894")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(nutrient_table)

    # ── Health Benefits ──
    benefits = data.get("health_benefits") or []
    if benefits:
        story.append(Paragraph("Health Benefits", section_style))
        for b in benefits:
            story.append(Paragraph(f"•  {b}", bullet_style))

    # ── Helpful For ──
    helpful = data.get("helpful_for") or []
    if helpful:
        story.append(Paragraph("Helpful For", section_style))
        for h in helpful:
            story.append(Paragraph(f"•  {h}", bullet_style))

    # ── Vitamins ──
    vitamins = data.get("vitamins") or []
    if vitamins:
        story.append(Paragraph("Vitamins &amp; Nutrients", section_style))
        vit_rows = [[v.get("name", ""), v.get("benefit", "")] for v in vitamins]
        vit_table = Table([["Vitamin/Compound", "Benefit"]] + vit_rows, colWidths=[2 * inch, 3.5 * inch])
        vit_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0984e3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(vit_table)

    # ── Warnings ──
    warnings = data.get("warnings") or {}
    if warnings:
        story.append(Paragraph("Warnings &amp; Precautions", section_style))
        warn_rows = [
            ("Diabetes", warnings.get("diabetes")),
            ("Allergy Warning", warnings.get("allergy")),
            ("Kidney Disease", warnings.get("kidney")),
        ]
        for label, text in warn_rows:
            if text:
                story.append(Paragraph(f"<b>{label}:</b> {text}", bullet_style))
        for other in (warnings.get("other") or []):
            story.append(Paragraph(f"<b>Other:</b> {other}", bullet_style))

    # ── Footer note ──
    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#e0e0e0"), thickness=1))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This report is generated by FruitAI's AI classification model and is for informational "
        "purposes only. Please consult a healthcare professional for medical advice.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#b2bec3")),
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
# ═══════════════════════════════════════════════
# ROUTES — Static pages
# ═══════════════════════════════════════════════
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "Fruit Classification.html")

@app.route("/auth.html")
def auth_page():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "auth.html")

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ═══════════════════════════════════════════════
# ROUTES — Health & Contact
# ═══════════════════════════════════════════════
@app.route("/api/health")
def health():
    return jsonify({"ok": model is not None,
                    "status": "ready" if model is not None else "degraded",
                    "model": "ResNet-50",
                    "database": "ready" if os.path.exists(DB_PATH) else "initializing"})

@app.route("/api/contact", methods=["POST"])
def contact():
    payload   = request.get_json(silent=True) or {}
    full_name = (payload.get("fullName") or "").strip()
    email     = (payload.get("email")    or "").strip()
    message   = (payload.get("message")  or "").strip()
    if not all([full_name, email, message]):
        return jsonify({"ok": False, "error": "All fields are required."}), 400

    current_user = require_user_token()
    user_id      = current_user["id"] if current_user else None

    with db_connect() as conn:
        conn.execute(
            "INSERT INTO feedback (user_id, full_name, email, message, created_at) VALUES (?,?,?,?,?)",
            (user_id, full_name, email, message, datetime.now(timezone.utc).isoformat()),
        )
    return jsonify({"ok": True})

# ═══════════════════════════════════════════════
# ROUTES — Admin
# ═══════════════════════════════════════════════
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    payload  = request.get_json(silent=True) or {}
    email    = (payload.get("email")    or "").strip().lower()
    password =  payload.get("password") or ""
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    with db_connect() as conn:
        user = conn.execute(
            "SELECT id, email, password_hash FROM admin_users WHERE email = ?", (email,)
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid admin credentials"}), 401
        token      = secrets.token_urlsafe(32)
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=12)).isoformat()
        conn.execute("INSERT INTO admin_sessions (admin_id, token, expires_at) VALUES (?, ?, ?)",
                     (user["id"], token, expires_at))
    return jsonify({"ok": True, "admin_key": token, "email": email})

@app.route("/api/admin/checked-images", methods=["GET"])
def admin_checked_images():
    admin_user = require_admin_token()
    if admin_user is None:
        return jsonify({"error": "Unauthorized"}), 401
    with db_connect() as conn:
        rows = conn.execute(
            "SELECT id,image_name,image_path,fruit_label,confidence,calories_per_100g,"
            "calories_source,created_at FROM checked_images ORDER BY id DESC LIMIT 120"
        ).fetchall()
    return jsonify({"ok": True, "admin": admin_user["email"], "checked_images": [
        {"id": r["id"], "image_name": r["image_name"], "image_url": r["image_path"],
         "fruit_name": r["fruit_label"].title().replace("_", " "),
         "confidence": r["confidence"], "calories_per_100g": r["calories_per_100g"],
         "calories_source": r["calories_source"], "created_at": r["created_at"]}
        for r in rows]})

@app.route("/api/admin/checked-images/<int:image_id>", methods=["DELETE"])
def admin_delete_checked_image(image_id):
    admin_user = require_admin_token()
    if admin_user is None:
        return jsonify({"error": "Unauthorized"}), 401
    with db_connect() as conn:
        row = conn.execute(
            "SELECT image_name FROM checked_images WHERE id=?", (image_id,)
        ).fetchone()
        if row is None:
            return jsonify({"ok": False, "error": "Image not found."}), 404
        conn.execute("DELETE FROM checked_images WHERE id=?", (image_id,))
    file_path = os.path.join(UPLOAD_DIR, row["image_name"])
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Could not remove file {file_path}: {e}")
    return jsonify({"ok": True})

@app.route("/api/admin/feedback/<int:feedback_id>", methods=["DELETE"])
def admin_delete_feedback(feedback_id):
    admin_user = require_admin_token()
    if admin_user is None:
        return jsonify({"error": "Unauthorized"}), 401
    with db_connect() as conn:
        row = conn.execute("SELECT id FROM feedback WHERE id=?", (feedback_id,)).fetchone()
        if row is None:
            return jsonify({"ok": False, "error": "Feedback not found."}), 404
        conn.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    return jsonify({"ok": True})

@app.route("/api/admin/users-history", methods=["GET"])
def admin_users_history():
    admin_user = require_admin_token()
    if admin_user is None:
        return jsonify({"error": "Unauthorized"}), 401
    with db_connect() as conn:
        # Any user who has EITHER a checked image OR a feedback submission
        user_ids = [row["user_id"] for row in conn.execute("""
            SELECT user_id FROM checked_images WHERE user_id IS NOT NULL
            UNION
            SELECT user_id FROM feedback WHERE user_id IS NOT NULL
        """).fetchall()]

        result = []
        for uid in user_ids:
            user = conn.execute(
                "SELECT id, username, email FROM users WHERE id=?", (uid,)
            ).fetchone()
            if user is None:
                continue
            images = conn.execute(
                "SELECT id,image_name,image_path,fruit_label,confidence,"
                "calories_per_100g,calories_source,created_at "
                "FROM checked_images WHERE user_id=? ORDER BY id DESC", (uid,)
            ).fetchall()
            feedbacks = conn.execute(
                "SELECT id, full_name, email, message, created_at "
                "FROM feedback WHERE user_id=? ORDER BY id DESC", (uid,)
            ).fetchall()
            timestamps = [i["created_at"] for i in images] + [f["created_at"] for f in feedbacks]
            result.append({
                "user_id": user["id"], "username": user["username"],
                "email": user["email"], "total_tests": len(images),
                "last_active": max(timestamps) if timestamps else None,
                "images": [{"id": i["id"], "image_url": i["image_path"],
                             "fruit_name": i["fruit_label"].title().replace("_", " "),
                             "confidence": i["confidence"],
                             "calories_per_100g": i["calories_per_100g"],
                             "calories_source": i["calories_source"],
                             "created_at": i["created_at"]} for i in images],
                "feedback": [{"id": f["id"], "full_name": f["full_name"], "email": f["email"],
                               "message": f["message"], "created_at": f["created_at"]} for f in feedbacks]})
        result.sort(key=lambda r: r["last_active"] or "", reverse=True)

        guest_images = conn.execute(
            "SELECT id,image_name,image_path,fruit_label,confidence,"
            "calories_per_100g,calories_source,created_at "
            "FROM checked_images WHERE user_id IS NULL ORDER BY id DESC"
        ).fetchall()
        guest_feedback = conn.execute(
            "SELECT id, full_name, email, message, created_at "
            "FROM feedback WHERE user_id IS NULL ORDER BY id DESC"
        ).fetchall()
        if guest_images or guest_feedback:
            timestamps = [i["created_at"] for i in guest_images] + [f["created_at"] for f in guest_feedback]
            result.append({
                "user_id": None, "username": "Guest (Not Logged In)", "email": "",
                "total_tests": len(guest_images),
                "last_active": max(timestamps) if timestamps else None,
                "images": [{"id": i["id"], "image_url": i["image_path"],
                             "fruit_name": i["fruit_label"].title().replace("_", " "),
                             "confidence": i["confidence"],
                             "calories_per_100g": i["calories_per_100g"],
                             "calories_source": i["calories_source"],
                             "created_at": i["created_at"]} for i in guest_images],
                "feedback": [{"id": f["id"], "full_name": f["full_name"], "email": f["email"],
                               "message": f["message"], "created_at": f["created_at"]} for f in guest_feedback]})
    return jsonify({"ok": True, "users": result})

# ═══════════════════════════════════════════════
# ROUTES — User Auth
# ═══════════════════════════════════════════════
@app.route("/api/signup", methods=["POST"])
def user_signup():
    payload  = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    email    = (payload.get("email")    or "").strip().lower()
    password =  payload.get("password") or ""
    if len(username) < 2:
        return jsonify({"ok": False, "error": "Name must be at least 2 characters."}), 400
    if "@" not in email:
        return jsonify({"ok": False, "error": "Enter a valid email address."}), 400
    if len(password) < 6:
        return jsonify({"ok": False, "error": "Password must be at least 6 characters."}), 400
    with db_connect() as conn:
        if conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            return jsonify({"ok": False, "error": "Email already registered."}), 409
        if conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone():
            return jsonify({"ok": False, "error": "Name already taken."}), 409
        conn.execute(
            "INSERT INTO users (username,email,password_hash,created_at) VALUES (?,?,?,?)",
            (username, email, generate_password_hash(password), datetime.now(timezone.utc).isoformat()))
    return jsonify({"ok": True, "message": f"Account created! Welcome, {username}!"})

@app.route("/api/login", methods=["POST"])
def user_login():
    payload  = request.get_json(silent=True) or {}
    email    = (payload.get("email")    or "").strip().lower()
    password =  payload.get("password") or ""
    remember =  payload.get("remember_me", False)
    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password are required."}), 400
    with db_connect() as conn:
        user = conn.execute(
            "SELECT id,username,email,password_hash FROM users WHERE email=?", (email,)
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify({"ok": False, "error": "Invalid email or password."}), 401
        token      = secrets.token_urlsafe(32)
        expires_at = (datetime.now(timezone.utc) + timedelta(days=30 if remember else 1)).isoformat()
        conn.execute("INSERT INTO user_sessions (user_id,token,expires_at) VALUES (?,?,?)",
                     (user["id"], token, expires_at))
    return jsonify({"ok": True, "token": token, "username": user["username"],
                    "email": user["email"], "message": f"Welcome back, {user['username']}!"})

@app.route("/api/logout", methods=["POST"])
def user_logout():
    token = request.headers.get("X-User-Token", "").strip()
    if token:
        with db_connect() as conn:
            conn.execute("DELETE FROM user_sessions WHERE token=?", (token,))
    return jsonify({"ok": True, "message": "Logged out."})

@app.route("/api/me", methods=["GET"])
def user_me():
    user = require_user_token()
    if user is None:
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True, "username": user["username"], "email": user["email"]})

# ═══════════════════════════════════════════════
# ROUTES — Google OAuth
# ═══════════════════════════════════════════════
@app.route("/auth/google/login")
def google_login():
    return google.authorize_redirect("http://127.0.0.1:5001/auth/google/callback")

@app.route("/auth/google/callback")
def google_callback():
    try:
        token    = google.authorize_access_token()
        userinfo = token.get("userinfo")
        if not userinfo:
            return "Google login failed.", 400
        email     = userinfo["email"]
        name      = userinfo.get("name", email.split("@")[0])
        google_id = userinfo["sub"]
        with db_connect() as conn:
            user = conn.execute("SELECT id,username,email FROM users WHERE email=?", (email,)).fetchone()
            if not user:
                conn.execute(
                    "INSERT INTO users (username,email,password_hash,created_at) VALUES (?,?,?,?)",
                    (name, email, generate_password_hash(google_id), datetime.now(timezone.utc).isoformat()))
                user = conn.execute("SELECT id,username,email FROM users WHERE email=?", (email,)).fetchone()
            session_token = secrets.token_urlsafe(32)
            expires_at    = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            conn.execute("INSERT INTO user_sessions (user_id,token,expires_at) VALUES (?,?,?)",
                         (user["id"], session_token, expires_at))
        return f"""<!DOCTYPE html><html><body><script>
            localStorage.setItem('fruitai_token',    '{session_token}');
            localStorage.setItem('fruitai_username', '{user['username']}');
            localStorage.setItem('fruitai_email',    '{user['email']}');
            window.location.href='/auth.html';
        </script></body></html>"""
    except Exception as e:
        return f"Google login error: {e}", 500

# ═══════════════════════════════════════════════
# ROUTES — AI Prediction  ← BOTH FIXES HERE
# ═══════════════════════════════════════════════
@app.route("/api/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "AI model not loaded"}), 500
    try:
        started = time.perf_counter()

        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files["image"]
        if image_file.mimetype not in ALLOWED_IMAGE_MIME:
            return jsonify({"error": "Unsupported format. Use JPG, PNG, or WEBP."}), 400

        image_bytes = image_file.read()
        if not image_bytes:
            return jsonify({"error": "Uploaded image is empty"}), 400

        # Validate it's a real image
        try:
            Image.open(io.BytesIO(image_bytes)).verify()
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            return jsonify({"error": "Invalid or corrupted image file"}), 400

        # FIX 2: Pre-resize before preprocessing → faster inference
        img_small = img.resize((224, 224), Image.BILINEAR)

        stored_name, image_url = save_uploaded_image(image_bytes, image_file.filename or "upload.png")

        # FIX 2: torch.inference_mode() is faster than no_grad
        inputs = preprocess_image(img_small)
        with torch.inference_mode():
            logits = model(**inputs).logits

        predicted_idx = torch.argmax(logits, dim=1).item()
        label         = model.config.id2label.get(predicted_idx, str(predicted_idx))
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        confidence    = float(probabilities[0][predicted_idx])

        label, confidence = maybe_override_strawberry(img, label, confidence)

        # FIX 1: Reject if not a known fruit/vegetable
        label_lower    = label.lower().replace("_", " ")
        is_known_fruit = any(fruit in label_lower for fruit in KNOWN_FRUIT_LABELS)

        if not is_known_fruit or confidence < CONFIDENCE_THRESHOLD:
            return jsonify({
                "error": "No fruit detected. Please upload a clear photo of a fruit or vegetable.",
                "error_type": "not_a_fruit",
                "detected_label": label,
                "confidence": round(confidence, 4),
            }), 422

        # FIX 2: Local nutrients lookup — zero network delay
        nutrients, cal_source = resolve_nutrients(label)
        processing_time_ms    = int((time.perf_counter() - started) * 1000)

        # Health Info: benefits, helpful-for conditions, vitamins, warnings
        health_info = get_health_info(label)

        current_user = require_user_token()
        user_id      = current_user["id"] if current_user else None
        record_checked_image(stored_name, image_url, label, confidence,
                             nutrients["calories"], cal_source, user_id)

        return jsonify({
            "fruit_name":         label.title().replace("_", " "),
            "confidence":         confidence,
            "calories_per_100g":  nutrients["calories"],
            "nutrients":          nutrients,
            "calories_source":    cal_source,
            "processing_time_ms": processing_time_ms,
            "image_url":          image_url,
            "health_benefits":    health_info["health_benefits"],
            "helpful_for":        health_info["helpful_for"],
            "vitamins":           health_info["vitamins"],
            "warnings":           health_info["warnings"],
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": "Failed to process image"}), 500

@app.route("/api/classify", methods=["POST"])
def classify():
    return predict()
@app.route("/api/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json(silent=True) or {}
    if not data.get("fruit_name"):
        return jsonify({"error": "No prediction data provided"}), 400
    try:
        pdf_buffer = build_pdf_report(data)
        safe_name = secure_filename(data.get("fruit_name", "report")) or "report"
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"FruitAI_Report_{safe_name}.pdf",
        )
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return jsonify({"error": "Failed to generate PDF report"}), 500
# ═══════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    # Runs once when gunicorn imports this module
    init_db()
