from pathlib import Path

# ==============================
# Project Paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "models"

ASSET_DIR = Path(__file__).resolve().parent / "assets"

# ==============================
# Dataset Paths
# ==============================

CLEAN_DATA = DATA_DIR / "cleaned" / "online_retail_cleaned.csv"

CUSTOMER_SEGMENTS = DATA_DIR / "processed" / "customer_segments.csv"

# ==============================
# Model Paths
# ==============================

SCALER_PATH = MODEL_DIR / "scaler.pkl"

KMEANS_MODEL_PATH = MODEL_DIR / "kmeans_model.pkl"

SIMILARITY_MATRIX_PATH = MODEL_DIR / "similarity_matrix.pkl"

PRODUCT_NAMES_PATH = MODEL_DIR / "product_names.pkl"

# ==============================
# Theme Colors
# ==============================

PRIMARY_COLOR = "#2E86C1"

SUCCESS_COLOR = "#27AE60"

WARNING_COLOR = "#F39C12"

DANGER_COLOR = "#E74C3C"

BACKGROUND = "#F8F9FA"