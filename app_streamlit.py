# -*- coding: utf-8 -*-
"""
💑 Bizim Market Paneli – Streamlit Versiyonu (München 🥨)
Ortak Market Harcaması, Fiş Takibi, Fiyat Kıyaslama & Enflasyon Analitiği
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import re
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Bizim Market Paneli 💑",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Adaptive CSS (Dark & Light Mode Friendly, No White-on-White Bugs!)
st.markdown("""
<style>
    /* Metric Cards Styling: Adaptive to Streamlit theme */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #10b981;
        transform: translateY(-2px);
    }
    div[data-testid="stMetric"] label {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        opacity: 0.85;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* 📱 Instagram-like Sleek, Compact Mobile UI */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        /* Make columns 2-by-2 grid instead of 100% full-screen vertical blocks */
        div[data-testid="column"] {
            min-width: calc(50% - 6px) !important;
            max-width: calc(50% - 6px) !important;
            flex: 1 1 calc(50% - 6px) !important;
            margin-bottom: 6px !important;
            padding: 0 2px !important;
        }
        /* Metric cards: Compact & Elegant */
        div[data-testid="stMetric"] {
            padding: 8px 10px !important;
            border-radius: 10px !important;
        }
        div[data-testid="stMetric"] label {
            font-size: 0.70rem !important;
            margin-bottom: 2px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.15rem !important;
            font-weight: 800 !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-size: 0.65rem !important;
        }
        /* Mobile Typography: Instagram-like readable sizes */
        h1 {
            font-size: 1.28rem !important;
            margin-bottom: 0.2rem !important;
        }
        h2 {
            font-size: 1.12rem !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.2rem !important;
        }
        h3 {
            font-size: 0.98rem !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.2rem !important;
        }
        h4, h5 {
            font-size: 0.86rem !important;
            margin-top: 0.3rem !important;
            margin-bottom: 0.15rem !important;
        }
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        div[data-testid="stCaptionContainer"],
        label, div[data-testid="stWidgetLabel"] p {
            font-size: 0.84rem !important;
            line-height: 1.35 !important;
        }
        /* Compact horizontal scrolling tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px !important;
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none !important;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 9px !important;
            font-size: 0.76rem !important;
            white-space: nowrap !important;
        }
        /* Compact multiselect & form inputs */
        div[data-baseweb="select"] {
            font-size: 0.82rem !important;
        }
        div[data-testid="stRadio"] label {
            padding: 2px 4px !important;
            font-size: 0.80rem !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        /* Compact tables & dataframes */
        div[data-testid="stDataFrame"] {
            font-size: 0.78rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========================================================
# 📲 MODERN APP SHELL: native-app look + installable (PWA) on phones
# ========================================================
st.markdown("""
<style>
    /* Hide Streamlit chrome so it feels like a real app */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }
    div[data-testid="stToolbar"], div[data-testid="stDecoration"], .stDeployButton { display: none !important; }
    .block-container { padding-top: 1.2rem !important; max-width: 1200px; }

    /* Modern surfaces */
    html, body, [class*="css"] { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }
    h1 { font-weight: 800 !important; letter-spacing: -0.02em; }
    h2, h3 { font-weight: 700 !important; letter-spacing: -0.01em; }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08) !important;
    }
    .stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
        border-radius: 12px !important; font-weight: 700 !important; min-height: 44px;
        transition: transform .12s ease, box-shadow .12s ease;
    }
    .stButton > button:active { transform: scale(0.97); }
    div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
        border-radius: 12px !important;
    }
    div[data-testid="stDataFrame"], div[data-testid="stExpander"] { border-radius: 14px; overflow: hidden; }
    div[data-testid="stExpander"] { border: 1px solid rgba(128,128,128,0.22); }

    /* Phone: safe-area + thumb-friendly sizing */
    @media (max-width: 768px) {
        .block-container { padding-bottom: calc(2.5rem + env(safe-area-inset-bottom)) !important; }
        .stButton > button { min-height: 46px; }
    }
</style>
""", unsafe_allow_html=True)

# Inject manifest / theme-color / iOS home-screen tags into the real <head>
components.html("""
<script>
(function () {
  try {
    const d = window.parent.document;
    const add = (tag, attrs) => {
      const key = Object.entries(attrs).map(([k, v]) => k + '=' + v).join('|');
      if (d.head.querySelector('[data-bm="' + key + '"]')) return;
      const el = d.createElement(tag);
      Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
      el.setAttribute('data-bm', key);
      d.head.appendChild(el);
    };
    add('link', { rel: 'manifest', href: '/app/static/manifest.json' });
    add('link', { rel: 'apple-touch-icon', href: '/app/static/apple-touch-icon.png' });
    add('meta', { name: 'apple-mobile-web-app-capable', content: 'yes' });
    add('meta', { name: 'mobile-web-app-capable', content: 'yes' });
    add('meta', { name: 'apple-mobile-web-app-title', content: 'Bizim Market' });
    add('meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'default' });
    d.title = 'Bizim Market';
  } catch (e) {}
})();
</script>
""", height=0)

# File Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "market_data.json")
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "market_data.csv")
MEAL_HISTORY_PATH = os.path.join(os.path.dirname(__file__), "data", "meal_history.json")
RECEIPTS_DIR = os.path.join(os.path.dirname(__file__), "public", "receipts")

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
os.makedirs(RECEIPTS_DIR, exist_ok=True)

def load_meal_history():
    if os.path.exists(MEAL_HISTORY_PATH):
        try:
            with open(MEAL_HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_meal_history(history_list):
    with open(MEAL_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history_list, f, ensure_ascii=False, indent=2)

# Brand Color Map
MARKET_COLORS = {
    "PENNY": "#cf0820",
    "HIT": "#e30613",
    "EDEKA": "#005ca9",
    "ALDI SÜD": "#002069",
    "dm": "#7b2b82",
    "tegut...": "#d97706",
    "Wolt Market": "#06b6d4",
    "Diğer": "#64748b"
}

MASTER_CATEGORIES = [
    "Et, Tavuk & Şarküteri",
    "Meyve & Sebze",
    "Süt, Peynir & Yumurta",
    "Fırın & Ekmek",
    "Temel Gıda & Makarna",
    "Konserve, Sos & Baharat",
    "Kahvaltılık",
    "Atıştırmalık & Tatlı",
    "İçecekler",
    "Dondurulmuş & Hazır Yemek",
    "Ev & Temizlik",
    "Kişisel Bakım",
    "Depozito",
    "Diğer"
]

# Normalization Helper
def clean_product_text(text):
    if not text:
        return ""
    t = re.sub(r'\s*\(\d+[\.,]?\d*\s*kg\)', '', text, flags=re.I)
    t = re.sub(r'\s*\d+[\.,]?\d*\s*kg\b', '', t, flags=re.I)
    t = re.sub(r'\s*\d+\s*g\b', '', t, flags=re.I)
    t = re.sub(r'\s*\d+[\.,]?\d*\s*L\b', '', t, flags=re.I)
    t = re.sub(r'\s*\d+\s*ml\b', '', t, flags=re.I)
    t = re.sub(r"\s*\d+['’]?[l|l]ı\b", '', t, flags=re.I)
    t = re.sub(r'\s*\d+\s*yıkama\b', '', t, flags=re.I)
    t = re.sub(r'\s*\d+\s*katlı\b', '', t, flags=re.I)
    t = re.sub(r'\s*\d+\s*stk\b', '', t, flags=re.I)
    return t.strip()

def normalize_product(raw_name, raw_brand="", raw_cat=""):
    name = (raw_name or "").strip()
    lower = name.lower()
    clean_name = clean_product_text(name)
    canonical = clean_name
    master_cat = "Diğer"

    # Et & Tavuk
    if any(k in lower for k in ["tavuk", "hähnchen", "pute", "hindi"]) and "kıyma" in lower:
        canonical = "Tavuk / Hindi Kıyma"
        master_cat = "Et, Tavuk & Şarküteri"
    elif any(k in lower for k in ["kıyma", "rd-hackfleisch", "hackfleisch", "rinderhack"]):
        canonical = "Dana Kıyma"
        master_cat = "Et, Tavuk & Şarküteri"
    elif any(k in lower for k in ["tavuk", "hähnchen", "hindi", "pute", "fileto", "filet"]):
        canonical = "Tavuk / Hindi Göğüs Fileto"
        master_cat = "Et, Tavuk & Şarküteri"
    elif "köfte" in lower:
        canonical = "Hazır Köfte Topları"
        master_cat = "Et, Tavuk & Şarküteri"
    elif any(k in lower for k in ["finesse", "salam", "jambon", "saftschinken"]):
        canonical = "Şarküteri (Salam / Jambon)"
        master_cat = "Et, Tavuk & Şarküteri"

    # Süt, Peynir & Yumurta
    elif any(k in lower for k in ["mitakos", "beyaz peynir", "süzme peynir", "weichkäs"]):
        canonical = "Beyaz Peynir (Mitakos)"
        master_cat = "Süt, Peynir & Yumurta"
    elif "emmental" in lower:
        canonical = "Emmental Peyniri"
        master_cat = "Süt, Peynir & Yumurta"
    elif "gouda" in lower:
        canonical = "Gouda Peyniri"
        master_cat = "Süt, Peynir & Yumurta"
    elif "cheddar" in lower:
        canonical = "Cheddar Peyniri"
        master_cat = "Süt, Peynir & Yumurta"
    elif "mozzarella" in lower:
        canonical = "Mozzarella Peyniri"
        master_cat = "Süt, Peynir & Yumurta"
    elif any(k in lower for k in ["yoğurt", "joghurt", "skyr"]):
        canonical = "Yunan Yoğurdu" if any(k in lower for k in ["griech", "yunan"]) else "Yoğurt"
        master_cat = "Süt, Peynir & Yumurta"
    elif any(k in lower for k in ["tereyağ", "butter", "kerrygold"]):
        canonical = "Tereyağı (Kerrygold)"
        master_cat = "Süt, Peynir & Yumurta"
    elif any(k in lower for k in ["yumurta", "eier"]):
        canonical = "Yumurta (10'lu)"
        master_cat = "Süt, Peynir & Yumurta"
    elif any(k in lower for k in ["krema", "sahne"]):
        canonical = "Krema (H-Sahne)"
        master_cat = "Süt, Peynir & Yumurta"
    elif any(k in lower for k in ["taze süt", "laktozsuz süt"]):
        canonical = "İnek Sütü"
        master_cat = "Süt, Peynir & Yumurta"

    # İçecekler
    elif any(k in lower for k in ["yulaf", "haferdr"]):
        canonical = "Yulaf Sütü Barista"
        master_cat = "İçecekler"
    elif "ayran" in lower:
        canonical = "Ayran"
        master_cat = "İçecekler"
    elif any(k in lower for k in ["şarap", "soave", "sauvignon", "pfalz"]):
        canonical = "Şarap"
        master_cat = "İçecekler"
    elif any(k in lower for k in ["bira", "hell", "augustiner"]):
        canonical = "Bira (Hell)"
        master_cat = "İçecekler"
    elif any(k in lower for k in ["spezi", "gazoz", "red bull", "enerji"]):
        canonical = "Gazoz & Enerji İçeceği"
        master_cat = "İçecekler"

    # Meyve & Sebze
    elif any(k in lower for k in ["muz", "bananen", "chiquita"]):
        canonical = "Muz"
        master_cat = "Meyve & Sebze"
    elif "domates" in lower and not any(k in lower for k in ["passata", "doğranmış", "püre"]):
        canonical = "Domates"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["salatalık", "minigurken"]):
        canonical = "Salatalık"
        master_cat = "Meyve & Sebze"
    elif "patates" in lower and "cips" not in lower:
        canonical = "Patates"
        master_cat = "Meyve & Sebze"
    elif "biber" in lower:
        canonical = "Biber"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["havuç", "karotten"]):
        canonical = "Havuç"
        master_cat = "Meyve & Sebze"
    elif "mantar" in lower:
        canonical = "Kültür Mantarı"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["soğan", "sarımsak"]):
        canonical = "Soğan & Sarımsak"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["şeftali", "ahududu"]):
        canonical = "Taze Meyve"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["zucchini", "kabak"]):
        canonical = "Kabak (Zucchini)"
        master_cat = "Meyve & Sebze"
    elif any(k in lower for k in ["feldsalat", "salata", "kuzu kulağı"]):
        canonical = "Yeşillik & Salata"
        master_cat = "Meyve & Sebze"

    # Fırın & Ekmek
    elif any(k in lower for k in ["baget", "steinofenbag", "ekmek", "bagel", "lavaş", "laugenstange", "schnitte"]):
        if any(k in lower for k in ["baget", "steinofen"]):
            canonical = "Taş Fırın Baget Ekmeği"
        elif "lavaş" in lower:
            canonical = "Protein Lavaş"
        elif "laugenstange" in lower:
            canonical = "Laugenstange (Simit)"
        else:
            canonical = "Ekmek & Fırın"
        master_cat = "Fırın & Ekmek"

    # Dondurulmuş
    elif "pizza" in lower:
        canonical = "Dondurulmuş Pizza"
        master_cat = "Dondurulmuş & Hazır Yemek"
    elif any(k in lower for k in ["bezelye", "dondurulmuş"]):
        canonical = "Dondurulmuş Sebze"
        master_cat = "Dondurulmuş & Hazır Yemek"

    # Atıştırmalık
    elif any(k in lower for k in ["cips", "kartoffelchips"]):
        canonical = "Patates Cipsi"
        master_cat = "Atıştırmalık & Tatlı"
    elif any(k in lower for k in ["çikolata", "kinder", "milka", "choviva"]):
        canonical = "Çikolata & Bar"
        master_cat = "Atıştırmalık & Tatlı"
    elif any(k in lower for k in ["kek", "madlen"]):
        canonical = "Kek & Bisküvi"
        master_cat = "Atıştırmalık & Tatlı"

    # Kahvaltılık
    elif any(k in lower for k in ["nutella", "fındık kreması"]):
        canonical = "Nutella / Fındık Kreması"
        master_cat = "Kahvaltılık"
    elif any(k in lower for k in ["kahve", "dolce gusto"]):
        canonical = "Kapsül Kahve"
        master_cat = "Kahvaltılık"
    elif any(k in lower for k in ["müsli", "granola"]):
        canonical = "Müsli & Granola"
        master_cat = "Kahvaltılık"
    elif any(k in lower for k in ["tahin", "tahini"]):
        canonical = "Tahin"
        master_cat = "Kahvaltılık"

    # Temel Gıda & Makarna
    elif any(k in lower for k in ["makarna", "fusilli", "rigatoni", "spag", "cornetti", "penne"]):
        canonical = "Makarna"
        master_cat = "Temel Gıda & Makarna"
    elif any(k in lower for k in ["kritharaki", "şehriye"]):
        canonical = "Arpa Şehriye / Kritharaki"
        master_cat = "Temel Gıda & Makarna"
    elif any(k in lower for k in ["pirinç", "mercimek", "fasulye", "bohnen"]):
        canonical = "Bakliyat (Pirinç/Mercimek/Fasulye)"
        master_cat = "Temel Gıda & Makarna"
    elif any(k in lower for k in ["un", "dinkel", "irmik", "hartweizen", "panko", "şeker"]):
        canonical = "Un, İrmik & Şeker"
        master_cat = "Temel Gıda & Makarna"
    elif any(k in lower for k in ["zeytinyağı", "sıvı yağ"]):
        canonical = "Zeytinyağı / Sıvı Yağ"
        master_cat = "Temel Gıda & Makarna"
    elif any(k in lower for k in ["leinsamen", "keten tohumu"]):
        canonical = "Keten Tohumu"
        master_cat = "Temel Gıda & Makarna"

    # Konserve & Sos
    elif any(k in lower for k in ["passata", "püre domates", "doğranmış domates"]):
        canonical = "Domates Püresi / Passata"
        master_cat = "Konserve, Sos & Baharat"
    elif any(k in lower for k in ["ketçap", "mayonez", "pesto", "soya sosu"]):
        canonical = "Soslar (Ketçap / Mayonez / Pesto)"
        master_cat = "Konserve, Sos & Baharat"
    elif any(k in lower for k in ["tuz", "kekik", "baharat", "sirke", "turşu"]):
        canonical = "Tuz, Baharat & Sirke"
        master_cat = "Konserve, Sos & Baharat"

    # Ev & Temizlik
    elif any(k in lower for k in ["tuvalet kağıdı", "deterjan", "çöp", "müllb", "temizlik", "bez", "kireç", "sprey", "klozet", "wc"]):
        if "tuvalet kağıdı" in lower:
            canonical = "Tuvalet Kağıdı"
        elif any(k in lower for k in ["çöp", "müllb"]):
            canonical = "Çöp Torbası"
        elif "deterjan" in lower:
            canonical = "Çamaşır Deterjanı"
        else:
            canonical = "Temizlik & Hijyen"
        master_cat = "Ev & Temizlik"

    # Kişisel Bakım
    elif any(k in lower for k in ["duş jeli", "sabun", "diş", "pamuk", "listerine", "aseton"]):
        canonical = "Diş Bakımı" if "diş" in lower else "Kişisel Bakım"
        master_cat = "Kişisel Bakım"

    # Depozito
    elif any(k in lower for k in ["pfand", "depozito"]):
        canonical = "Depozito (Pfand)"
        master_cat = "Depozito"
    elif any(k in lower for k in ["poşet", "tasche"]):
        canonical = "Alışveriş Poşeti"
        master_cat = "Diğer"
    elif any(k in lower for k in ["mum", "ampul", "sürahi", "brita", "kap"]):
        canonical = "Ev & Mutfak Gereçleri"
        master_cat = "Ev & Mutfak Gereçleri"
    elif raw_cat and raw_cat != "Diğer":
        master_cat = raw_cat

    return canonical, master_cat

# Load Data
@st.cache_data(ttl=2)
def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            df["tarih_dt"] = pd.to_datetime(df["tarih"])
            if "kanonik_urun" not in df.columns:
                df["kanonik_urun"] = df["urun"]
            return df
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Veritabanı dosyası bulunamadı!")
    st.stop()

# Helper: Save Data & Sync CSV
def save_items_to_db(items_list):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(items_list, f, ensure_ascii=False, indent=2)
    # Also save CSV
    save_df = pd.DataFrame(items_list)
    save_df.to_csv(CSV_PATH, sep=";", index=False, encoding="utf-8-sig")
    st.cache_data.clear()

# ========================================================
# SIDEBAR: FILTERS & FAST FILE UPLOADER
# ========================================================
with st.sidebar:
    st.markdown("### 💑 Bizim Market")
    st.caption("München Alışveriş & Fiş Takip Paneli")
    st.markdown("---")

    # Fast Multi-format Uploader in Sidebar (Receipt Images or Tables)
    st.subheader("📸 Hızlı Fiş / Veri Yükle")
    side_table_file = st.file_uploader(
        "Kasa Fişi Fotoğrafı veya Excel/CSV:",
        type=["png", "jpg", "jpeg", "webp", "xlsx", "csv", "xls"],
        key="side_file"
    )

    if side_table_file:
        file_ext = os.path.splitext(side_table_file.name)[1].lower()
        if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
            st.session_state["uploaded_receipt_bytes"] = side_table_file.getvalue()
            st.session_state["uploaded_receipt_name"] = side_table_file.name
            st.image(side_table_file, caption=f"📸 {side_table_file.name}", use_container_width=True)
            st.success("✅ Fiş fotoğrafı yüklendi! Sağdaki **'📸 Fiş Yükleme & Akıllı Giriş'** sekmesinden kalemleri kaydedebilirsiniz.")
        elif file_ext in [".xlsx", ".csv", ".xls"]:
            try:
                if file_ext == ".csv":
                    new_df = pd.read_csv(side_table_file, sep=None, engine="python")
                else:
                    new_df = pd.read_excel(side_table_file)

                st.write(f"Bulunan satır sayısı: {len(new_df)}")
                if st.button("✅ Tabloyu Veritabanına Aktar", key="btn_side_import"):
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        curr_items = json.load(f)
                    max_id = max([it.get("id", 0) for it in curr_items]) if curr_items else 0
                    
                    added_count = 0
                    for _, row in new_df.iterrows():
                        max_id += 1
                        u_name = str(row.get("Ürün Adı", row.get("urun", "Ürün")))
                        c_name, m_cat = normalize_product(u_name)
                        item_dict = {
                            "id": max_id,
                            "tarih": str(row.get("Tarih", row.get("tarih", datetime.now().strftime("%Y-%m-%d")))),
                            "market": str(row.get("Market", row.get("market", "Diğer"))),
                            "urun": u_name,
                            "kanonik_urun": c_name,
                            "marka": str(row.get("Marka", row.get("marka", ""))),
                            "kategori": m_cat,
                            "miktar": float(row.get("Miktar", row.get("miktar", 1))),
                            "birim_fiyat": float(row.get("Birim Fiyat (€)", row.get("birim_fiyat", 0))),
                            "toplam_fiyat": float(row.get("Toplam Fiyat (€)", row.get("toplam_fiyat", 0))),
                            "kdv": str(row.get("KDV Grubu", row.get("kdv", "B (7%)"))),
                            "fis_no": str(row.get("Fiş No", row.get("fis_no", ""))),
                            "odeyen": str(row.get("Ödeyen", row.get("odeyen", "Ortak")))
                        }
                        curr_items.insert(0, item_dict)
                        added_count += 1
                    save_items_to_db(curr_items)
                    st.success(f"{added_count} ürün başarıyla eklendi!")
                    st.rerun()
            except Exception as e:
                st.error(f"Hata: {e}")

    st.markdown("---")
    st.subheader("🔍 Filtreler")

    date_preset = st.radio(
        "Zaman Aralığı:",
        ["Tümü", "Bu Ay (Ekim 2026)", "Geçen Ay (Eylül 2026)", "Son 7 Gün"],
        index=0
    )

    all_stores = ["Tümü"] + sorted(list(df["market"].dropna().unique()))
    selected_store = st.selectbox("🏪 Market:", all_stores)

    all_cats = ["Tümü"] + sorted(list(df["kategori"].dropna().unique()))
    selected_cat = st.selectbox("📦 Kategori:", all_cats)

    all_payers = ["Tümü"] + sorted(list(df["odeyen"].dropna().unique()))
    selected_payer = st.selectbox("👤 Kim Ödedi?:", all_payers)

    search_query = st.text_input("🔎 Ürün veya Marka Ara:", placeholder="Örn: kıyma, yumurta, süt...").strip().lower()

    st.markdown("---")
    st.markdown("### ⚙️ Aylık Bütçe Hedefi")
    budget_goal = st.number_input("Hedef Bütçe (€):", min_value=100.0, max_value=2000.0, value=450.0, step=25.0)

# Apply Filters
filtered_df = df.copy()

if date_preset == "Bu Ay (Ekim 2026)":
    filtered_df = filtered_df[filtered_df["tarih"].str.startswith("2026-10")]
elif date_preset == "Geçen Ay (Eylül 2026)":
    filtered_df = filtered_df[filtered_df["tarih"].str.startswith("2026-09")]
elif date_preset == "Son 7 Gün":
    filtered_df = filtered_df[filtered_df["tarih_dt"] >= pd.to_datetime("2026-10-22")]

if selected_store != "Tümü":
    filtered_df = filtered_df[filtered_df["market"] == selected_store]

if selected_cat != "Tümü":
    filtered_df = filtered_df[filtered_df["kategori"] == selected_cat]

if selected_payer != "Tümü":
    filtered_df = filtered_df[filtered_df["odeyen"] == selected_payer]

if search_query:
    filtered_df = filtered_df[
        filtered_df["urun"].str.lower().str.contains(search_query, na=False) |
        filtered_df["kanonik_urun"].str.lower().str.contains(search_query, na=False) |
        filtered_df["marka"].str.lower().str.contains(search_query, na=False) |
        filtered_df["market"].str.lower().str.contains(search_query, na=False)
    ]

# ========================================================
# HEADER & BUDGET BANNER
# ========================================================
st.title("🛒 Bizim Market Paneli – München 🥨")
st.caption("Kız arkadaşınızla ortak harcama, fiş arşivleme ve market fiyat kıyaslama sistemi")

oct_spend = df[df["tarih"].str.startswith("2026-10")]["toplam_fiyat"].sum()
budget_pct = min(100.0, (oct_spend / budget_goal) * 100) if budget_goal > 0 else 0
remaining_budget = budget_goal - oct_spend

col_b1, col_b2, col_b3 = st.columns([2, 1, 1])
with col_b1:
    st.markdown(f"**🎯 Ekim Ayı Ortak Bütçesi:** €{oct_spend:,.2f} / **€{budget_goal:,.2f}** (`%{budget_pct:.0f}` kullanıldı)")
    st.progress(budget_pct / 100.0)
with col_b2:
    if remaining_budget >= 0:
        st.markdown(f"<span style='color:#10b981; font-weight:700;'>Kalan Bütçe:</span> €{remaining_budget:,.2f}", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:#ef4444; font-weight:700;'>Bütçe Aşıldı:</span> -€{abs(remaining_budget):,.2f}", unsafe_allow_html=True)
with col_b3:
    sep_spend = df[df["tarih"].str.startswith("2026-09")]["toplam_fiyat"].sum()
    st.markdown(f"**Geçen Ay (Eylül):** €{sep_spend:,.2f}")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ========================================================
# 🏠 DOLAPTAKİ HAZIR YEMEKLERİMİZ WIDGET (BİTTİ Mİ KONTROLÜ)
# ========================================================
all_meal_records = load_meal_history()
active_home_meals = [m for m in all_meal_records if m.get("durum", "aktif") == "aktif"]

if active_home_meals:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 78, 59, 0.3)); border: 1px solid #10b981; border-radius: 12px; padding: 8px 12px; margin-bottom: 8px;">
        <span style="font-weight: 700; color: #34d399; font-size: 0.92rem;">🍲 Dolapta Hazır Yemeğimiz Var! (Önce Bunları Bitirelim)</span>
    </div>
    """, unsafe_allow_html=True)
    
    for hm in active_home_meals:
        hm_c1, hm_c2 = st.columns([5, 1])
        with hm_c1:
            st.markdown(f"**🍲 {hm.get('yemek')}** (`{hm.get('porsiyon_gun', '2 gün')}` • {hm.get('tarih')} • *{hm.get('kim_yapti', 'Birlikte')}*)")
            if hm.get("not") and hm.get("not") != "Afiyet olsun!":
                st.caption(f"📝 *Not: {hm.get('not')}*")
        with hm_c2:
            if st.button("✅ Bitti!", key=f"btn_finish_top_{hm.get('id')}", use_container_width=True, help="Yemek bittiyse tıklayın, dolaptan düşsün"):
                hm["durum"] = "bitti"
                save_meal_history(all_meal_records)
                st.success(f"'{hm.get('yemek')}' bitti olarak işaretlendi!")
                st.rerun()
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ========================================================
# KPI METRICS ROW
# ========================================================
total_spend = filtered_df["toplam_fiyat"].sum()
total_items = len(filtered_df)
receipt_count = filtered_df["fis_no"].replace("", pd.NA).dropna().nunique()
avg_basket = total_spend / receipt_count if receipt_count > 0 else 0

pfand_df = filtered_df[
    filtered_df["kategori"].str.lower().str.contains("depozito", na=False) |
    filtered_df["urun"].str.lower().str.contains("pfand", na=False)
]
pfand_net = pfand_df["toplam_fiyat"].sum()

store_grp = filtered_df.groupby("market")["toplam_fiyat"].sum()
top_store_name = store_grp.idxmax() if not store_grp.empty else "-"
top_store_val = store_grp.max() if not store_grp.empty else 0

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("Toplam Harcama", f"€{total_spend:,.2f}", delta=f"{total_items} ürün")
kpi2.metric("Ortalama Fiş", f"€{avg_basket:,.2f}", delta=f"{receipt_count} fiş")
kpi3.metric("Ekim Harcaması", f"€{oct_spend:,.2f}", delta=f"Eylül €{sep_spend:,.0f}")
kpi4.metric("Lider Market", top_store_name, delta=f"€{top_store_val:,.1f}")
kpi5.metric("Pfand (Depozito)", f"€{pfand_net:,.2f}", delta="Net İade/Ödeme")
kpi6.metric("Kayıtlı Fiş", f"{receipt_count} Adet", delta="Münih Kasa")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# ========================================================
# TABS: STRUCTURED PROFESSIONAL ANALYTICS
# ========================================================
tab_overview, tab_stores, tab_radar, tab_planner, tab_gallery, tab_add = st.tabs([
    "📊 Genel Bakış & Trendler",
    "🏪 Market & Kategori Dağılımı",
    "🥩 Akıllı Fiyat Radarı (Kıyaslama)",
    "🍽️ Haftalık Menü & Bütçe Planı",
    "🖼️ Orijinal Fiş Galerisi",
    "📸 Fiş Yükle / Yeni Alışveriş Ekle"
])

# --------------------------------------------------------
# TAB 1: GENEL BAKIŞ & TRENDLER
# --------------------------------------------------------
with tab_overview:
    r1_col1, r1_col2 = st.columns([3, 2])

    with r1_col1:
        st.subheader("📅 Günlük Harcama & Kümülatif Trend")
        daily_df = filtered_df.groupby("tarih_dt")["toplam_fiyat"].sum().reset_index()
        daily_df = daily_df.sort_values("tarih_dt")
        daily_df["kumulatif"] = daily_df["toplam_fiyat"].cumsum()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=daily_df["tarih_dt"],
            y=daily_df["toplam_fiyat"],
            name="Günlük Harcama (€)",
            marker_color="#10b981",
            opacity=0.85
        ))
        fig_trend.add_trace(go.Scatter(
            x=daily_df["tarih_dt"],
            y=daily_df["kumulatif"],
            name="Kümülatif Toplam (€)",
            yaxis="y2",
            line=dict(color="#38bdf8", width=3)
        ))

        fig_trend.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Günlük (€)", showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
            yaxis2=dict(title="Kümülatif (€)", overlaying="y", side="right", showgrid=False),
            xaxis=dict(showgrid=False),
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with r1_col2:
        st.subheader("📆 Haftanın Günleri Harcama Dağılımı")
        day_df = filtered_df.copy()
        day_order = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        tr_days = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
        day_df["gun"] = day_df["tarih_dt"].dt.dayofweek.map(tr_days)
        day_spend = day_df.groupby("gun")["toplam_fiyat"].sum().reindex(day_order).fillna(0).reset_index()

        fig_days = px.bar(
            day_spend, x="gun", y="toplam_fiyat",
            labels={"gun": "", "toplam_fiyat": "Harcama (€)"},
            color="toplam_fiyat",
            color_continuous_scale="Purples"
        )
        fig_days.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=20, b=20),
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="rgba(128,128,128,0.15)")
        )
        st.plotly_chart(fig_days, use_container_width=True)

    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.subheader("👥 Harcamayı Kim Yaptı?")
        payer_spend = filtered_df.groupby("odeyen")["toplam_fiyat"].sum().reset_index()
        fig_payer = px.pie(
            payer_spend, names="odeyen", values="toplam_fiyat",
            color="odeyen",
            color_discrete_map={"Ortak": "#10b981", "Ben": "#0284c7", "Kız Arkadaşım": "#ec4899"},
            hole=0.45
        )
        fig_payer.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_payer, use_container_width=True)

    with r2_col2:
        st.subheader("🧾 Almanya KDV Grubu (%7 Gıda vs %19 Standart)")
        def clean_vat(v):
            v_str = str(v).upper()
            if "7" in v_str or "B" in v_str:
                return "%7 (İndirimli Temel Gıda)"
            elif "19" in v_str or "A" in v_str:
                return "%19 (Genel Standart KDV)"
            return "%7 (Diğer)"
        vat_df = filtered_df.copy()
        vat_df["kdv_temiz"] = vat_df["kdv"].apply(clean_vat)
        vat_spend = vat_df.groupby("kdv_temiz")["toplam_fiyat"].sum().reset_index()

        fig_vat = px.pie(
            vat_spend, names="kdv_temiz", values="toplam_fiyat",
            color_discrete_sequence=["#10b981", "#f59e0b", "#6366f1"],
            hole=0.45
        )
        fig_vat.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_vat, use_container_width=True)

# --------------------------------------------------------
# TAB 2: MARKET & KATEGORİ DAĞILIMI
# --------------------------------------------------------
with tab_stores:
    c_m1, c_m2 = st.columns(2)

    with c_m1:
        st.subheader("🏪 Marketlerin Harcama Payları")
        market_spend = filtered_df.groupby("market")["toplam_fiyat"].sum().reset_index()
        fig_market = px.pie(
            market_spend, names="market", values="toplam_fiyat",
            color="market",
            color_discrete_map=MARKET_COLORS,
            hole=0.55
        )
        fig_market.update_traces(textposition='inside', textinfo='percent+label')
        fig_market.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=20, b=20),
            legend=dict(orientation="h", y=-0.1),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_market, use_container_width=True)

    with c_m2:
        st.subheader("📦 Standart Ana Kategoriler (Top 10)")
        cat_spend = filtered_df.groupby("kategori")["toplam_fiyat"].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_cat = px.bar(
            cat_spend, x="toplam_fiyat", y="kategori", orientation="h",
            labels={"toplam_fiyat": "Toplam Harcama (€)", "kategori": ""},
            color="toplam_fiyat",
            color_continuous_scale="Tealgrn"
        )
        fig_cat.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=20, b=20),
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(128,128,128,0.15)")
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("📊 Market & Kategori Çapraz Harcama Tablosu")
    pivot_df = filtered_df.pivot_table(index="market", columns="kategori", values="toplam_fiyat", aggfunc="sum", fill_value=0)
    st.dataframe(pivot_df.style.format("€{:.2f}"), use_container_width=True)

# --------------------------------------------------------
# TAB 3: AKILLI FİYAT RADARI
# --------------------------------------------------------
with tab_radar:
    st.subheader("🔍 Akıllı Ürün Fiyat Radarı & Karşılaştırma")
    st.caption("Gramaj farkları ve kasa isimleri filtrelenerek ürünlerin marketler arası fiyat farkı kıyaslanır.")

    popular_staples = [
        "Dana Kıyma", "Tavuk / Hindi Göğüs Fileto", "Yumurta (10'lu)",
        "Yulaf Sütü Barista", "Muz", "Tereyağı (Kerrygold)", "Patates Cipsi",
        "Beyaz Peynir (Mitakos)", "Emmental Peyniri", "Yunan Yoğurdu",
        "Nutella / Fındık Kreması", "Makarna", "Dondurulmuş Pizza", "Ayran"
    ]
    all_canonicals = sorted(list(set(popular_staples + list(df["kanonik_urun"].dropna().unique()))))
    selected_product = st.selectbox("🎯 Karşılaştırılacak Ürünü Seçin:", all_canonicals, index=0)

    match_df = df[
        (df["kanonik_urun"].str.lower() == selected_product.lower()) |
        (df["urun"].str.lower().str.contains(selected_product.lower(), na=False))
    ].copy()

    if not match_df.empty:
        min_price = match_df["birim_fiyat"].min()
        min_row = match_df.loc[match_df["birim_fiyat"].idxmin()]
        max_price = match_df["birim_fiyat"].max()
        max_row = match_df.loc[match_df["birim_fiyat"].idxmax()]
        avg_price = match_df["birim_fiyat"].mean()
        price_diff_pct = ((max_price - min_price) / min_price * 100) if min_price > 0 else 0

        rc1, rc2, rc3 = st.columns(3)
        rc1.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius: 12px; padding: 16px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #10b981; text-transform: uppercase;">🏆 En Ucuz Market</div>
            <div style="font-size: 1.5rem; font-weight: 800; margin-top: 4px;">{min_row['market']}</div>
            <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.9;">Birim Fiyat: €{min_price:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        rc2.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 12px; padding: 16px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #ef4444; text-transform: uppercase;">📈 En Pahalı Market</div>
            <div style="font-size: 1.5rem; font-weight: 800; margin-top: 4px;">{max_row['market']}</div>
            <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.9;">Birim Fiyat: €{max_price:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        rc3.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 12px; padding: 16px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #f59e0b; text-transform: uppercase;">💡 Fiyat Farkı & Tasarruf</div>
            <div style="font-size: 1.5rem; font-weight: 800; margin-top: 4px;">%{price_diff_pct:.0f} Fark</div>
            <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.9;">Ortalama: €{avg_price:.2f} ({len(match_df)} alım)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        fig_radar = px.scatter(
            match_df.sort_values("tarih_dt"),
            x="tarih_dt",
            y="birim_fiyat",
            color="market",
            size="miktar",
            color_discrete_map=MARKET_COLORS,
            hover_data=["urun", "market", "miktar", "birim_fiyat", "toplam_fiyat", "fis_no"],
            labels={"birim_fiyat": "Birim Fiyat (€)", "tarih_dt": "Tarih", "market": "Market"}
        )
        fig_radar.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_radar.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="rgba(128,128,128,0.15)")
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("##### 🧾 Fiyat Geçmişi Detayları:")
        st.dataframe(
            match_df[["tarih", "market", "kanonik_urun", "urun", "miktar", "birim_fiyat", "toplam_fiyat", "fis_no"]]
            .sort_values("tarih", ascending=False),
            use_container_width=True
        )
    else:
        st.info("Bu ürün için henüz kayıt bulunamadı.")

# --------------------------------------------------------
# TAB 4: GÜNÜN & HAFTANIN MENÜSÜ (ÇORBA + ANA YEMEK + SALATA)
# --------------------------------------------------------
with tab_planner:
    st.subheader("🍽️ Günün & Haftanın Menüsü: Çorba + Ana Yemek + Salata")
    st.caption("Sevgilinizle akşam ne pişireceğinizi belirleyin; sistem çorba, ana yemek ve salatanın malzemelerini birleştirip kilerdeki eksikleri çıkarsın.")

    # 1. EXPANDED RECIPES DATABASE CATEGORIZED BY COURSE
    COURSE_DATABASE = {
        # 🥣 ÇORBALAR
        "soups": {
            "Kırmızı Mercimek Çorbası": {
                "days": 2, "category": "Çorba",
                "ingredients": [
                    {"name": "Kırmızı Mercimek (300g)", "qty": 0.6, "unit": "paket", "market": "PENNY", "cost": 0.85},
                    {"name": "Kuru Soğan", "qty": 0.2, "unit": "kg", "market": "PENNY", "cost": 0.40},
                    {"name": "Havuç (1 adet)", "qty": 0.15, "unit": "kg", "market": "PENNY", "cost": 0.25},
                    {"name": "Patates (1 adet)", "qty": 0.15, "unit": "kg", "market": "PENNY", "cost": 0.20},
                    {"name": "Tereyağı & Nane", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Tarhana Çorbası": {
                "days": 2, "category": "Çorba",
                "ingredients": [
                    {"name": "Tarhana (Kiler/Evden)", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.00},
                    {"name": "Tereyağı & Salça", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.40}
                ]
            },
            "Kaşarlı Domates Çorbası": {
                "days": 2, "category": "Çorba",
                "ingredients": [
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Rendelenmiş Kaşar / Emmental", "qty": 0.3, "unit": "paket", "market": "PENNY", "cost": 0.60},
                    {"name": "Süt & Tereyağı & Un", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.40}
                ]
            },
            "Yayla Çorbası (Naneli)": {
                "days": 2, "category": "Çorba",
                "ingredients": [
                    {"name": "Yoğurt (Körfez / Griechischer)", "qty": 0.4, "unit": "kg", "market": "PENNY", "cost": 0.90},
                    {"name": "Pirinç (3 kaşık)", "qty": 0.1, "unit": "paket", "market": "Kiler", "cost": 0.20},
                    {"name": "Tereyağı & Nane", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Tavuk Suyu Şehriye Çorbası": {
                "days": 2, "category": "Çorba",
                "ingredients": [
                    {"name": "Tavuk Göğsü (Haşlamalık)", "qty": 0.3, "unit": "paket", "market": "PENNY", "cost": 1.20},
                    {"name": "Arpa / Tel Şehriye (Kritharaki)", "qty": 0.2, "unit": "paket", "market": "PENNY", "cost": 0.30},
                    {"name": "Limon & Maydanoz", "qty": 1, "unit": "porsiyon", "market": "PENNY", "cost": 0.50}
                ]
            }
        },

        # 🍲 ANA YEMEKLER
        "mains": {
            # 3 Günlük Bereketli Tencere Yemekleri
            "Kuru Fasülye (Pirinç Pilavlı)": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Kuru Fasulye (500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.29},
                    {"name": "Pirinç (Baldo/Jasmin 500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.29},
                    {"name": "Kuru Soğan", "qty": 0.3, "unit": "kg", "market": "PENNY", "cost": 0.60},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Tereyağı & Sıvı Yağ", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.40}
                ]
            },
            "Bezelye Pilavı (Havuçlu)": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Dondurulmuş / Konserve Bezelye", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.19},
                    {"name": "Pirinç (Baldo/Jasmin 500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.29},
                    {"name": "Havuç", "qty": 0.25, "unit": "kg", "market": "PENNY", "cost": 0.45},
                    {"name": "Tereyağı", "qty": 1, "unit": "porsiyon", "market": "PENNY", "cost": 0.50}
                ]
            },
            "Zeytinyağlı Kabak Yemeği": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Kabak (Zucchini)", "qty": 1.0, "unit": "kg (~3-4 adet)", "market": "PENNY", "cost": 1.49},
                    {"name": "Kuru Soğan", "qty": 0.3, "unit": "kg", "market": "PENNY", "cost": 0.60},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Pirinç (2 kaşık)", "qty": 0.1, "unit": "paket", "market": "Kiler", "cost": 0.20}
                ]
            },
            "Tavuk Pilav (Didiklenmiş Tavuklu)": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Tavuk Göğüs Fileto (600g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 4.50},
                    {"name": "Pirinç (Baldo/Jasmin 500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.29},
                    {"name": "Tereyağı & Sıvı Yağ", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.50}
                ]
            },
            "Patates Yemeği (Tencere Usulü)": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Patates (1.2 kg)", "qty": 1.2, "unit": "kg", "market": "PENNY", "cost": 1.40},
                    {"name": "Kuru Soğan", "qty": 0.3, "unit": "kg", "market": "PENNY", "cost": 0.60},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Sıvı Yağ & Biber", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Zeytinyağlı Taze Yeşil Fasülye": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Taze Yeşil Fasulye (Greenland)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.29},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Kuru Soğan", "qty": 0.3, "unit": "kg", "market": "PENNY", "cost": 0.60},
                    {"name": "Zeytinyağı", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.40}
                ]
            },
            "Sebzeli Tavuk Sote": {
                "days": 3, "type": "3 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Tavuk Göğüs Fileto (600g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 4.50},
                    {"name": "Biber (Kırmızı / Yeşil)", "qty": 0.4, "unit": "kg", "market": "PENNY", "cost": 1.20},
                    {"name": "Kültür Mantarı (250g)", "qty": 0.6, "unit": "paket", "market": "HIT/PENNY", "cost": 1.30},
                    {"name": "Kuru Soğan & Sarımsak", "qty": 0.3, "unit": "kg", "market": "PENNY", "cost": 0.60}
                ]
            },

            # 2 Günlük Pratik & Özel Akşam Yemekleri
            "Kıymalı Makarna (Bolonez Soslu)": {
                "days": 2, "type": "2 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Dana Kıyma (400-500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 5.49},
                    {"name": "Makarna (Penne/Fusilli 500g)", "qty": 1, "unit": "paket", "market": "PENNY/HIT", "cost": 0.99},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Kuru Soğan & Sarımsak", "qty": 0.2, "unit": "kg", "market": "PENNY", "cost": 0.40}
                ]
            },
            "Mantar Soslu Tavuk & Patates Püresi": {
                "days": 2, "type": "2 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Tavuk Göğüs Fileto (500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 3.80},
                    {"name": "Kültür Mantarı (300-400g)", "qty": 1, "unit": "paket", "market": "HIT/PENNY", "cost": 2.19},
                    {"name": "Krema (H-Sahne 200ml)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69},
                    {"name": "Patates (1 kg püre için)", "qty": 1.0, "unit": "kg", "market": "PENNY", "cost": 1.20},
                    {"name": "Süt & Tereyağı", "qty": 1, "unit": "porsiyon", "market": "PENNY", "cost": 0.80}
                ]
            },
            "Fırında Lazanya": {
                "days": 2, "type": "2 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Dana Kıyma (400-500g)", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 5.49},
                    {"name": "Lazanya Yaprakları", "qty": 1, "unit": "paket", "market": "PENNY/EDEKA", "cost": 1.49},
                    {"name": "Domates Püresi (Passata - 2 kutu)", "qty": 2, "unit": "kutu", "market": "PENNY", "cost": 1.38},
                    {"name": "Rendelenmiş Kaşar / Emmental", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.79},
                    {"name": "Süt, Un & Tereyağı (Beşamel)", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 1.20}
                ]
            },
            "Sebzeli & Tavuklu Noodle": {
                "days": 2, "type": "2 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Noodle (2-3 paket)", "qty": 2, "unit": "paket", "market": "PENNY/HIT", "cost": 1.98},
                    {"name": "Tavuk Göğsü (Didiklenmiş)", "qty": 0.4, "unit": "paket", "market": "PENNY", "cost": 1.50},
                    {"name": "Garnitür Sebze (Havuç, Biber, Kabak)", "qty": 1, "unit": "porsiyon", "market": "PENNY", "cost": 1.20},
                    {"name": "Soya Sosu / Sıvı Yağ", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.40}
                ]
            },
            "Fırında Kaşarlı Köfte & Patates": {
                "days": 2, "type": "2 Günlük", "category": "Ana Yemek",
                "ingredients": [
                    {"name": "Dana Kıyma veya Hazır Köfte", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 4.99},
                    {"name": "Patates (1 kg)", "qty": 1.0, "unit": "kg", "market": "PENNY", "cost": 1.20},
                    {"name": "Rendelenmiş Kaşar / Gouda", "qty": 0.5, "unit": "paket", "market": "PENNY", "cost": 0.90},
                    {"name": "Domates Püresi (Passata)", "qty": 1, "unit": "kutu", "market": "PENNY", "cost": 0.69}
                ]
            }
        },

        # 🥗 SALATALAR & YAN LEZZETLER
        "sides": {
            "Çoban / Gavurdağı Salatası": {
                "days": 1, "category": "Salata",
                "ingredients": [
                    {"name": "Salkım / Mini Domates", "qty": 0.5, "unit": "kg", "market": "PENNY", "cost": 1.29},
                    {"name": "Salatalık (Gurke 2 adet)", "qty": 2, "unit": "adet", "market": "PENNY", "cost": 0.98},
                    {"name": "Biber (1 adet)", "qty": 0.2, "unit": "kg", "market": "PENNY", "cost": 0.60},
                    {"name": "Kuru Soğan", "qty": 0.1, "unit": "kg", "market": "PENNY", "cost": 0.20},
                    {"name": "Zeytinyağı & Limon", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Akdeniz Yeşillik Salatası (Feldsalat)": {
                "days": 1, "category": "Salata",
                "ingredients": [
                    {"name": "Akdeniz Yeşilliği / Feldsalat", "qty": 1, "unit": "paket", "market": "PENNY", "cost": 1.39},
                    {"name": "Beyaz Peynir (Mitakos)", "qty": 0.3, "unit": "paket", "market": "PENNY", "cost": 0.60},
                    {"name": "Zeytinyağı & Balzamik / Limon", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Havuç Tarator (Yoğurtlu)": {
                "days": 1, "category": "Meze",
                "ingredients": [
                    {"name": "Havuç (4-5 adet)", "qty": 0.5, "unit": "kg", "market": "PENNY", "cost": 0.85},
                    {"name": "Yoğurt (Körfez / Griechischer)", "qty": 0.4, "unit": "kg", "market": "PENNY", "cost": 0.90},
                    {"name": "Sarımsak & Zeytinyağı", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Salatalıklı Cacık (Naneli)": {
                "days": 1, "category": "Meze",
                "ingredients": [
                    {"name": "Salatalık (Gurke 2 adet)", "qty": 2, "unit": "adet", "market": "PENNY", "cost": 0.98},
                    {"name": "Yoğurt (Körfez / Griechischer)", "qty": 0.4, "unit": "kg", "market": "PENNY", "cost": 0.90},
                    {"name": "Sarımsak, Zeytinyağı & Nane", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Kuru Fasülye Yanı Piyaz": {
                "days": 1, "category": "Salata",
                "ingredients": [
                    {"name": "Haşlanmış Kuru Fasulye", "qty": 0.5, "unit": "paket", "market": "PENNY", "cost": 0.65},
                    {"name": "Kuru Soğan & Maydanoz", "qty": 0.2, "unit": "kg", "market": "PENNY", "cost": 0.40},
                    {"name": "Zeytinyağı, Sumak & Limon", "qty": 1, "unit": "porsiyon", "market": "Kiler", "cost": 0.30}
                ]
            },
            "Yoğurtlu Kabak / Köz Biber Mezesi": {
                "days": 1, "category": "Meze",
                "ingredients": [
                    {"name": "Kabak (2 adet) veya Köz Biber", "qty": 0.6, "unit": "kg", "market": "PENNY", "cost": 0.90},
                    {"name": "Yoğurt (Körfez / Griechischer)", "qty": 0.4, "unit": "kg", "market": "PENNY", "cost": 0.90},
                    {"name": "Dereotu & Sarımsak", "qty": 1, "unit": "porsiyon", "market": "PENNY", "cost": 0.40}
                ]
            }
        }
    }

    # Pantry Lookup Function using Munich Purchase History
    PANTRY_KEYWORDS = {
        "Kuru Fasulye (500g)": ["fasulye", "bohnen"],
        "Haşlanmış Kuru Fasulye": ["fasulye", "bohnen"],
        "Taze Yeşil Fasulye (Greenland)": ["fasulye", "bohnen"],
        "Dondurulmuş / Konserve Bezelye": ["bezelye", "erbsen"],
        "Kabak (Zucchini)": ["kabak", "zucchini"],
        "Kabak (2 adet) veya Köz Biber": ["kabak", "zucchini", "biber"],
        "Tavuk Göğüs Fileto (600g)": ["tavuk", "fileto", "hähnchen", "pute"],
        "Tavuk Göğüs Fileto (500g)": ["tavuk", "fileto", "hähnchen", "pute"],
        "Tavuk Göğsü (Haşlamalık)": ["tavuk", "fileto", "hähnchen"],
        "Tavuk Göğsü (Didiklenmiş)": ["tavuk", "fileto", "hähnchen"],
        "Patates (1.2 kg)": ["patates", "kartoffel"],
        "Patates (1 kg püre için)": ["patates", "kartoffel"],
        "Patates (1 kg)": ["patates", "kartoffel"],
        "Patates (1 adet)": ["patates", "kartoffel"],
        "Dana Kıyma (400-500g)": ["kıyma", "hackfleisch", "rinderhack"],
        "Dana Kıyma veya Hazır Köfte": ["kıyma", "köfte", "hackfleisch"],
        "Makarna (Penne/Fusilli 500g)": ["makarna", "fusilli", "penne", "spagh", "rigatoni"],
        "Lazanya Yaprakları": ["lazanya", "lasagne"],
        "Noodle (2-3 paket)": ["noodle"],
        "Arpa / Tel Şehriye (Kritharaki)": ["kritharaki", "şehriye", "reisn"],
        "Kültür Mantarı (300-400g)": ["mantar", "champignon"],
        "Kültür Mantarı (250g)": ["mantar", "champignon"],
        "Krema (H-Sahne 200ml)": ["h-sahne", "sahne", "krema"],
        "Kırmızı Mercimek (300g)": ["mercimek", "linsen"],
        "Tarhana (Kiler/Evden)": ["tarhana"],
        "Rendelenmiş Kaşar / Emmental": ["peynir", "emmental", "gouda", "kaşar"],
        "Rendelenmiş Kaşar / Gouda": ["peynir", "emmental", "gouda", "kaşar"],
        "Beyaz Peynir (Mitakos)": ["mitakos", "peynir", "weichkäs"],
        "Yoğurt (Körfez / Griechischer)": ["yoğurt", "joghurt", "körfez", "skyr"],
        "Pirinç (Baldo/Jasmin 500g)": ["pirinç", "reis", "kritharaki"],
        "Pirinç (2 kaşık)": ["pirinç", "reis"],
        "Pirinç (3 kaşık)": ["pirinç", "reis"],
        "Kuru Soğan": ["soğan", "zwiebel"],
        "Kuru Soğan & Sarımsak": ["soğan", "sarımsak", "zwiebel"],
        "Kuru Soğan & Maydanoz": ["soğan", "zwiebel"],
        "Havuç": ["havuç", "karotten"],
        "Havuç (1 adet)": ["havuç", "karotten"],
        "Havuç (4-5 adet)": ["havuç", "karotten"],
        "Salatalık (Gurke 2 adet)": ["salatalık", "gurke"],
        "Salkım / Mini Domates": ["domates", "tomaten"],
        "Biber (Kırmızı / Yeşil)": ["biber", "paprika"],
        "Biber (1 adet)": ["biber", "paprika"],
        "Akdeniz Yeşilliği / Feldsalat": ["feldsalat", "salata", "yeşillik"],
        "Domates Püresi (Passata)": ["passata", "püre domates", "salça"],
        "Domates Püresi (Passata - 2 kutu)": ["passata", "püre domates", "salça"],
        "Tereyağı": ["tereyağ", "butter", "kerrygold"],
        "Tereyağı & Nane": ["tereyağ", "butter", "nane"],
        "Tereyağı & Salça": ["tereyağ", "butter", "salça"],
        "Tereyağı & Sıvı Yağ": ["tereyağ", "butter", "yağ"],
        "Süt & Tereyağı": ["süt", "milch", "tereyağ"],
        "Süt & Tereyağı & Un": ["süt", "milch", "un", "tereyağ"],
        "Süt, Un & Tereyağı (Beşamel)": ["süt", "milch", "un", "tereyağ"]
    }

    def get_pantry_status(ing_name, dataframe):
        keys = PANTRY_KEYWORDS.get(ing_name, [w.lower() for w in ing_name.split() if len(w) > 3])
        matches = []
        for _, row in dataframe.iterrows():
            text = f"{str(row.get('kanonik_urun', ''))} {str(row.get('urun', ''))}".lower()
            if "cips" in text and "patates" in ing_name.lower():
                continue
            if "fındık" in text and ("krema" in ing_name.lower() or "peynir" in ing_name.lower()):
                continue
            if any(k in text for k in keys):
                matches.append(row)
        if matches:
            last_m = sorted(matches, key=lambda x: str(x.get("tarih", "")), reverse=True)[0]
            t_str = str(last_m.get("tarih", ""))
            try:
                t_dt = pd.to_datetime(t_str)
                days_ago = (datetime.now() - t_dt).days
                days_text = f"{days_ago} gün önce" if days_ago >= 0 else "yakın zamanda"
            except:
                days_ago = 0
                days_text = ""
            market = str(last_m.get("market", ""))
            u_name = str(last_m.get("urun", ""))
            return {
                "found": True,
                "date": t_str,
                "days_ago": days_ago,
                "days_text": days_text,
                "market": market,
                "item": u_name
            }
        return {"found": False}

    # 2. QUICK SET MENU COMBOS (HAZIR UYUMLU MENÜLER)
    st.markdown("#### 🌟 1. Hızlı Set Menü Kombosu Seçin (veya Aşağıdan Serbest Oluşturun):")
    
    preset_choice = st.radio(
        "Hazır Uyumlu Menü Şablonu:",
        [
            "🎨 Kendi Menümü Kendim Oluşturacağım (Serbest Seçim)",
            "🍲 1. Geleneksel Tencere Menüsü: Mercimek Çorbası (2G) + Kuru Fasülye & Pilav (3G) + Çoban Salata (1G)",
            "🍗 2. Restoran Usulü Özel Menü: Kaşarlı Domates Çorbası (2G) + Mantar Soslu Tavuk & Püre (2G) + Akdeniz Salatası (1G)",
            "🍝 3. İtalyan Akşamı Menüsü: Tarhana Çorbası (2G) + Fırında Lazanya (2G) + Havuç Tarator (1G)",
            "🥗 4. Hafif & Diyet Menüsü: Yayla Çorbası (2G) + Zeytinyağlı Kabak Yemeği (3G) + Salatalıklı Cacık (1G)",
            "🍜 5. Pratik & Hızlı Menü: Tavuk Suyu Şehriye Çorbası (2G) + Sebzeli Noodle (2G) + Gavurdağı Salatası (1G)"
        ],
        index=0
    )

    # Determine default selections based on preset
    def_soups = []
    def_mains = []
    def_sides = []

    if "1. Geleneksel Tencere" in preset_choice:
        def_soups = ["Kırmızı Mercimek Çorbası"]
        def_mains = ["Kuru Fasülye (Pirinç Pilavlı)"]
        def_sides = ["Çoban / Gavurdağı Salatası"]
    elif "2. Restoran Usulü" in preset_choice:
        def_soups = ["Kaşarlı Domates Çorbası"]
        def_mains = ["Mantar Soslu Tavuk & Patates Püresi"]
        def_sides = ["Akdeniz Yeşillik Salatası (Feldsalat)"]
    elif "3. İtalyan Akşamı" in preset_choice:
        def_soups = ["Tarhana Çorbası"]
        def_mains = ["Fırında Lazanya"]
        def_sides = ["Havuç Tarator (Yoğurtlu)"]
    elif "4. Hafif & Diyet" in preset_choice:
        def_soups = ["Yayla Çorbası (Naneli)"]
        def_mains = ["Zeytinyağlı Kabak Yemeği"]
        def_sides = ["Salatalıklı Cacık (Naneli)"]
    elif "5. Pratik & Hızlı" in preset_choice:
        def_soups = ["Tavuk Suyu Şehriye Çorbası"]
        def_mains = ["Sebzeli & Tavuklu Noodle"]
        def_sides = ["Çoban / Gavurdağı Salatası"]
    else:
        def_soups = ["Kırmızı Mercimek Çorbası"]
        def_mains = ["Kuru Fasülye (Pirinç Pilavlı)", "Mantar Soslu Tavuk & Patates Püresi"]
        def_sides = ["Salatalıklı Cacık (Naneli)"]

    # 🔄 SYNC PRESET TO SESSION STATE SO MULTISELECT UPDATES IMMEDIATELY ON CLICK
    if "active_preset_tracker" not in st.session_state:
        st.session_state["active_preset_tracker"] = preset_choice
        st.session_state["ms_soups"] = def_soups
        st.session_state["ms_mains"] = def_mains
        st.session_state["ms_sides"] = def_sides
    elif st.session_state["active_preset_tracker"] != preset_choice:
        st.session_state["active_preset_tracker"] = preset_choice
        st.session_state["ms_soups"] = def_soups
        st.session_state["ms_mains"] = def_mains
        st.session_state["ms_sides"] = def_sides

    st.markdown("---")
    st.markdown("#### 🍱 2. Günün & Haftanın Menü Bileşenleri:")

    c_soup, c_main, c_side = st.columns(3)

    with c_soup:
        st.markdown("##### 🥣 1. Çorba Seçimi:")
        selected_soups = st.multiselect(
            "Çorba(lar):",
            list(COURSE_DATABASE["soups"].keys()),
            key="ms_soups"
        )
        for s in selected_soups:
            s_days = COURSE_DATABASE["soups"][s].get("days", 2)
            st.caption(f"🥣 **{s}** -> `{s_days} Günlük` tencere")

    with c_main:
        st.markdown("##### 🍲 2. Ana Yemek Seçimi:")
        selected_mains = st.multiselect(
            "Ana Yemek(ler):",
            list(COURSE_DATABASE["mains"].keys()),
            key="ms_mains"
        )
        for m in selected_mains:
            m_days = COURSE_DATABASE["mains"][m].get("days", 2)
            m_type = COURSE_DATABASE["mains"][m].get("type", "2 Günlük")
            st.caption(f"🍲 **{m}** -> `{m_days} Gün Gider` ({m_type})")

    with c_side:
        st.markdown("##### 🥗 3. Salata & Meze Seçimi:")
        selected_sides = st.multiselect(
            "Salata / Meze(ler):",
            list(COURSE_DATABASE["sides"].keys()),
            key="ms_sides"
        )
        for d in selected_sides:
            d_days = COURSE_DATABASE["sides"][d].get("days", 1)
            st.caption(f"🥗 **{d}** -> `{d_days} Günlük` taze meze")

    all_selected_dishes = []
    dish_meta_map = {}

    for s_name in selected_soups:
        all_selected_dishes.append(s_name)
        dish_meta_map[s_name] = COURSE_DATABASE["soups"][s_name]

    for m_name in selected_mains:
        all_selected_dishes.append(m_name)
        dish_meta_map[m_name] = COURSE_DATABASE["mains"][m_name]

    for d_name in selected_sides:
        all_selected_dishes.append(d_name)
        dish_meta_map[d_name] = COURSE_DATABASE["sides"][d_name]

    st.markdown("---")

    # 3. DAYS CALCULATION & MONTHLY BUDGET PROJECTION
    if all_selected_dishes:
        # Calculate days per course
        soup_days = sum([COURSE_DATABASE["soups"][s].get("days", 2) for s in selected_soups])
        main_days = sum([COURSE_DATABASE["mains"][m].get("days", 2) for m in selected_mains])
        side_days = sum([COURSE_DATABASE["sides"][d].get("days", 1) for d in selected_sides])
        effective_days = max(main_days, 1)

        # Collect raw ingredients & costs
        ing_dict = {}
        course_cost_breakdown = {}

        for dish_name in all_selected_dishes:
            d_data = dish_meta_map[dish_name]
            d_cost = sum([ing["cost"] for ing in d_data["ingredients"]])
            course_cost_breakdown[dish_name] = {
                "name": dish_name,
                "category": d_data.get("category", "Yemek"),
                "days": d_data.get("days", 2),
                "cost": d_cost
            }
            for ing in d_data["ingredients"]:
                i_name = ing["name"]
                if i_name not in ing_dict:
                    ing_dict[i_name] = {
                        "name": i_name,
                        "qty": ing["qty"],
                        "unit": ing["unit"],
                        "market": ing["market"],
                        "cost": ing["cost"],
                        "dishes": [dish_name]
                    }
                else:
                    ing_dict[i_name]["qty"] += ing["qty"]
                    ing_dict[i_name]["cost"] += ing["cost"]
                    ing_dict[i_name]["dishes"].append(dish_name)

        gross_total = sum([info["cost"] for info in ing_dict.values()])

        st.markdown("### ⏳ 3. Parça Parça Gün Hesabı & 30 Günlük Aylık Bütçe Planı")
        st.caption("Seçtiğiniz yemeklerin kaçar gün gideceği ve buna göre 30 günlük aylık mutfak bütçesi simülasyonu:")

        # Day Breakdown Cards
        dc1, dc2, dc3, dc4 = st.columns(4)
        dc1.metric("🍲 Ana Yemek Süresi", f"{main_days} Gün", f"{len(selected_mains)} Çeşit Ana Yemek")
        dc2.metric("🥣 Çorba Süresi", f"{soup_days} Gün", f"{len(selected_soups)} Çeşit Çorba")
        dc3.metric("🥗 Salata & Meze", f"{side_days} Gün", f"{len(selected_sides)} Çeşit Salata")
        dc4.metric("📅 Toplam Kapsanan Gün", f"{effective_days} Gün", "30 Günlük Aylık Plandan")

        # Item by Item Days Table
        breakdown_rows = []
        for d_name, d_info in course_cost_breakdown.items():
            portions = d_info["days"] * 2
            breakdown_rows.append({
                "Öğün / Yemek": d_name,
                "Kategori": d_info["category"],
                "Kaç Gün Gider?": f"{d_info['days']} Gün",
                "Toplam Porsiyon (2 Kişi)": f"{portions} Porsiyon",
                "Tahmini Maliyet": f"€{d_info['cost']:.2f}",
                "Günlük Maliyeti": f"€{(d_info['cost']/d_info['days']):.2f} / gün"
            })
        st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True)

        st.markdown("---")

        # 4. SHOPPING LIST WITH PANTRY DETECTION & REAL-TIME SAVINGS
        st.markdown("### 🛒 4. Menü Alışveriş Listesi & 'Evde Olabilir' Kontrolü")
        st.caption("Çorba, ana yemek ve salatanın ortak malzemeleri toplanmış ve geçmiş Münih fişlerinize göre evde olma ihtimali olanlar listelenmiştir:")

        pantry_savings = 0.0
        active_items = []
        pantry_items = []

        # Header bar
        st.markdown("<div style='background: rgba(128,128,128,0.12); padding: 8px 14px; border-radius: 8px; font-weight: 700; display: flex; justify-content: space-between;'><span>Malzeme & Kullanılacağı Yemekler</span><span>Önerilen Market & Tutar</span></div>", unsafe_allow_html=True)

        for i_idx, (i_name, info) in enumerate(ing_dict.items()):
            pantry_info = get_pantry_status(i_name, df)

            col_i1, col_i2 = st.columns([3, 2])
            with col_i1:
                qty_str = f"{info['qty']:.1f} {info['unit']}" if isinstance(info['qty'], float) and info['qty'] % 1 != 0 else f"{int(info['qty'])} {info['unit']}"
                st.markdown(f"**{info['name']}** (`{qty_str}`) — *Kullanım: {', '.join(info['dishes'])}*")
                if pantry_info["found"]:
                    st.caption(f"💡 **Evde Olabilir:** En son **{pantry_info['date']}** ({pantry_info['days_text']}) **{pantry_info['market']}**'den alınmıştı: *'{pantry_info['item']}'*")

            with col_i2:
                in_pantry = st.checkbox("✅ Evde Zaten Var (Listeden Çıkar)", key=f"menu_pantry_{i_idx}")
                st.markdown(f"🏪 **{info['market']}** • **€{info['cost']:.2f}**")

            if in_pantry:
                pantry_savings += info["cost"]
                pantry_items.append(f"{info['name']} ({qty_str})")
            else:
                active_items.append({
                    "name": info["name"],
                    "qty": qty_str,
                    "market": info["market"],
                    "cost": info["cost"]
                })
            st.markdown("<hr style='margin: 4px 0; border: none; border-top: 1px solid rgba(128,128,128,0.15);'/>", unsafe_allow_html=True)

        net_total = max(0.0, gross_total - pantry_savings)
        daily_couple_cost = (net_total / effective_days) if effective_days > 0 else 0
        monthly_simulated_spend = daily_couple_cost * 30
        budget_usage_pct = (monthly_simulated_spend / budget_goal * 100) if budget_goal > 0 else 0
        remaining_monthly_free = budget_goal - monthly_simulated_spend

        # Budget & Monthly Simulation Metrics
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("💰 Bu Menü Net Tutarı", f"€{net_total:,.2f}", f"Evden €{pantry_savings:,.2f} Tasarruf!", delta_color="normal")
        m2.metric("📅 Günlük Yemek Maliyeti", f"€{daily_couple_cost:,.2f} / gün", "2 Kişi Akşam Yemeği")
        m3.metric("🎯 30 Günlük Aylık Projeksiyon", f"€{monthly_simulated_spend:,.2f}", f"Bütçenin %{budget_usage_pct:.0f}'i", delta_color="normal" if monthly_simulated_spend <= budget_goal else "inverse")
        m4.metric("👛 Kalan Serbest Bütçe", f"€{remaining_monthly_free:,.2f}", f"Hedef: €{budget_goal:.0f}", delta_color="normal")

        # Monthly Budget Progress Bar
        st.markdown(f"**🎯 30 Günlük Aylık Bütçe Uyumu:** Bu menü temposunda giderseniz aylık yemek masrafınız **€{monthly_simulated_spend:,.2f}** olur (Aylık hedefiniz olan **€{budget_goal:,.2f}** içinde son derece rahat kalırsınız).")
        st.progress(min(1.0, max(0.0, budget_usage_pct / 100.0)))

        # WhatsApp Ready Format
        wa_text = f"*💑 BİZİM GÜNÜN & HAFTANIN MENÜSÜ ({effective_days} GÜNLÜK)*\n\n"
        wa_text += f"*🍲 Ana Yemek ({main_days} Gün):* {', '.join(selected_mains) if selected_mains else 'Seçilmedi'}\n"
        wa_text += f"*🥣 Çorba ({soup_days} Gün):* {', '.join(selected_soups) if selected_soups else 'Seçilmedi'}\n"
        wa_text += f"*🥗 Salata & Meze ({side_days} Gün):* {', '.join(selected_sides) if selected_sides else 'Seçilmedi'}\n\n"
        wa_text += f"*💰 Bu Dönem Net Tutar:* €{net_total:,.2f} *(Günlük sadece €{daily_couple_cost:.2f} / 2 kişi)*\n"
        wa_text += f"*🎯 30 Günlük Tahmini Aylık Mutfak:* €{monthly_simulated_spend:.2f} *(Hedef bütçe €{budget_goal:.0f})*\n\n"
        
        wa_text += "*🛒 SATIN ALINACAK EKSİKLER:*\n"
        for it in active_items:
            wa_text += f"- [ ] {it['name']} ({it['qty']}) -> {it['market']} (~€{it['cost']:.2f})\n"
        
        if pantry_items:
            wa_text += "\n*🏠 EVDE OLANLAR (Alınmayacak!):*\n"
            for p_it in pantry_items:
                wa_text += f"- [x] {p_it}\n"
        
        wa_text += f"\n📍 Not: Bu menü bizi {effective_days} gün rahat götürür! Tok karnına alışverişe gidelim 😊"

        with st.expander("📲 Sevgiline WhatsApp'tan Göndermek İçin Menü & Listeyi Kopyala", expanded=True):
            st.code(wa_text, language="text")

    # ----------------------------------------------------
    # 5. GERÇEKTEN BU YEMEĞİ YAPTIK & GEÇMİŞ NOTLARI
    # ----------------------------------------------------
    st.markdown("---")
    st.markdown("### 🍳 5. 'Bu Yemeği Yaptık & Bitti' Günlüğü")
    st.caption("Planladığınız veya evde yaptığınız yemekleri 'pişirildi / bitti' olarak işaretleyip kimin yaptığı, kaç gün sürdüğü ve lezzet notlarınızı kaydedebilirsiniz.")

    meal_history = load_meal_history()

    # Form to add new cooked meal
    with st.expander("➕ Yeni Pişirilen Yemeği Kaydet", expanded=(len(meal_history) == 0)):
        with st.form("form_cooked_meal", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                # Suggest from active selected dishes first, then all dishes
                cook_dish_options = all_selected_dishes.copy() if 'all_selected_dishes' in locals() and all_selected_dishes else []
                all_available_dishes = list(COURSE_DATABASE["mains"].keys()) + list(COURSE_DATABASE["soups"].keys()) + list(COURSE_DATABASE["sides"].keys())
                for d in all_available_dishes:
                    if d not in cook_dish_options:
                        cook_dish_options.append(d)
                cook_dish_options.append("Diğer (Özel Tarif)")

                c_dish = st.selectbox("🍳 Pişirilen Yemek:", cook_dish_options)
                c_custom_dish = st.text_input("Özel Yemek Adı (Eğer Diğer seçtiyseniz):") if c_dish == "Diğer (Özel Tarif)" else ""

            with f_col2:
                c_date = st.date_input("📅 Pişirme / Tüketim Tarihi:", datetime.now())
                c_chef = st.selectbox("👩‍🍳 Kim Pişirdi?:", ["Birlikte 💑", "Ben 👨‍🍳", "Kız Arkadaşım 👩‍🍳"])

            with f_col3:
                c_duration = st.selectbox("⏳ Kaç Gün Yetti / Sürdü?:", ["1 gün", "2 gün", "3 gün", "4 gün", "5+ gün"], index=1)
                c_rating = st.selectbox("⭐ Lezzet / Memnuniyet:", ["⭐⭐⭐⭐⭐ (Efsane oldu!)", "⭐⭐⭐⭐ (Çok lezzetli)", "⭐⭐⭐ (İyiydi)", "⭐⭐ (Geliştirilmeli)"], index=0)

            c_status_choice = st.selectbox("🍲 Yemek Durumu:", ["Dolapta Hazır (Hala Yeniyor) 🟢", "Yendi & Bitti ⚪"], index=0)
            c_notes = st.text_area("📝 Notlar & Hatırlatmalar:", placeholder="Örn: Tuzu ve baharatı tam kıvamındaydı, 3 gün rahat yettik. Bir dahakine yanına cacık da yapalım.")

            submit_cooked = st.form_submit_button("💾 Yemeği Geçmişe Kaydet & Arşivle", type="primary", use_container_width=True)
            if submit_cooked:
                final_dish_name = c_custom_dish.strip() if (c_dish == "Diğer (Özel Tarif)" and c_custom_dish.strip()) else c_dish
                new_entry = {
                    "id": int(datetime.now().timestamp()),
                    "tarih": str(c_date),
                    "yemek": final_dish_name,
                    "kim_yapti": c_chef,
                    "porsiyon_gun": c_duration,
                    "puan": c_rating.split(" ")[0],
                    "durum": "aktif" if "Dolapta" in c_status_choice else "bitti",
                    "not": c_notes.strip() if c_notes else "Afiyet olsun!"
                }
                meal_history.insert(0, new_entry)
                save_meal_history(meal_history)
                st.success(f"🎉 Harika! '{final_dish_name}' yemeği başarıyla geçmiş günlüğüne kaydedildi!")
                st.rerun()

    # Display History
    if meal_history:
        st.markdown("##### 📖 Geçmişte Pişirilen Yemekler:")

        # Summary stats
        h_col1, h_col2, h_col3 = st.columns(3)
        h_col1.metric("Toplam Pişirilen Yemek", f"{len(meal_history)} Defa", "Ev Yemeği Keyfi 🍲")
        
        birlikte_count = sum(1 for m in meal_history if "Birlikte" in m.get("kim_yapti", ""))
        ben_count = sum(1 for m in meal_history if "Ben" in m.get("kim_yapti", ""))
        kiz_count = sum(1 for m in meal_history if "Kız" in m.get("kim_yapti", ""))
        
        h_col2.metric("Şef Dağılımı", f"💑 {birlikte_count} | 👨‍🍳 {ben_count} | 👩‍🍳 {kiz_count}", "Tatlı Mutfak Ortaklığı")
        
        # Most cooked dish
        dish_counts = {}
        for m in meal_history:
            y = m.get("yemek", "")
            dish_counts[y] = dish_counts.get(y, 0) + 1
        fav_dish = max(dish_counts, key=dish_counts.get) if dish_counts else "-"
        h_col3.metric("En Çok Yapılan", fav_dish, f"{dish_counts.get(fav_dish, 0)} kez pişirildi")

        # Show active meals cards with finish button
        active_in_history = [m for m in meal_history if m.get("durum", "bitti") == "aktif"]
        if active_in_history:
            st.markdown("###### 🟢 Şu An Dolapta Hazır Olanlar (Tükendikçe 'Bitti'ye basın):")
            for a_h in active_in_history:
                ah_c1, ah_c2 = st.columns([5, 1])
                with ah_c1:
                    st.markdown(f"**🍲 {a_h.get('yemek')}** ({a_h.get('porsiyon_gun', '2 gün')} • {a_h.get('tarih')} • *{a_h.get('kim_yapti', 'Birlikte')}*)")
                with ah_c2:
                    if st.button("✅ Bitti!", key=f"btn_finish_hist_{a_h.get('id')}", use_container_width=True):
                        a_h["durum"] = "bitti"
                        save_meal_history(meal_history)
                        st.success(f"'{a_h.get('yemek')}' bitti olarak işaretlendi!")
                        st.rerun()

        # History Dataframe
        history_df = pd.DataFrame(meal_history)
        if "durum" not in history_df.columns:
            history_df["durum"] = "bitti"
        history_df["durum_badge"] = history_df["durum"].map(lambda x: "🟢 Dolapta Var" if x == "aktif" else "⚪ Bitti")
        display_hist = history_df[["tarih", "yemek", "durum_badge", "kim_yapti", "porsiyon_gun", "puan", "not"]].copy()
        display_hist.columns = ["Tarih", "Yemek Adı", "Durum", "Kimin Eline Sağlık?", "Kaç Gün Gitti?", "Puan", "Notlar"]
        st.dataframe(display_hist, use_container_width=True)
    else:
        st.info("Henüz geçmişe kaydedilmiş yemek bulunmuyor. Yaptığınız yemekleri yukarıdaki butondan kaydedebilirsiniz!")

# --------------------------------------------------------
# TAB 5: ORİJİNAL FİŞ GALERİSİ
# --------------------------------------------------------
with tab_gallery:
    st.subheader("🖼️ Münih Kasa Fişleri Fotoğraf Galerisi")
    st.caption("Yüklenen orijinal kasa fişlerinin fotoğrafları")

    receipt_images = [
        {"file": "receipt_2026-10-29_7965.png", "title": "PENNY • 29.10.2026 (#7965)", "total": "€27.08"},
        {"file": "receipt_2026-10-28_7449.png", "title": "PENNY • 28.10.2026 (#7449)", "total": "€16.99"},
        {"file": "receipt_2026-10-26_1053.png", "title": "PENNY • 26.10.2026 (#1053)", "total": "€17.40"},
        {"file": "receipt_2026-10-26_5573.png", "title": "PENNY • 26.10.2026 (#5573)", "total": "€9.14"},
        {"file": "receipt_2026-10-22_5950.png", "title": "PENNY • 22.10.2026 (#5950)", "total": "€5.27"}
    ]

    gal_cols = st.columns(len(receipt_images))
    for idx, r_info in enumerate(receipt_images):
        with gal_cols[idx]:
            img_path = os.path.join(RECEIPTS_DIR, r_info["file"])
            if os.path.exists(img_path):
                st.image(img_path, caption=f"{r_info['title']} - {r_info['total']}", use_container_width=True)
            else:
                st.info(f"{r_info['title']}\n{r_info['total']}")

# --------------------------------------------------------
# TAB 5: FİŞ YÜKLE / YENİ ALIŞVERİŞ EKLE (TAM ÇALIŞAN ENTEGRASYON)
# --------------------------------------------------------
with tab_add:
    st.subheader("📸 Fiş Yükleme & Akıllı Giriş Merkezi")
    st.caption("Fiş fotoğrafını telefon kamerasından çekebilir, galeriden yükleyebilir veya kalemleri hızlıca ekleyebilirsiniz.")

    # 1. Image Capture / Upload Options
    receipt_image_bytes = st.session_state.get("uploaded_receipt_bytes", None)
    receipt_filename = st.session_state.get("uploaded_receipt_name", None)

    if receipt_image_bytes:
        st.info(f"💡 Sol menüden seçilen fiş görseli hazır: **{receipt_filename}**")
        st.image(receipt_image_bytes, caption="Yüklenen Kasa Fişi", width=260)
        if st.button("🗑️ Bu Görseli Değiştir / Kaldır", key="btn_clear_uploaded_img"):
            st.session_state.pop("uploaded_receipt_bytes", None)
            st.session_state.pop("uploaded_receipt_name", None)
            st.rerun()

    input_method = st.radio(
        "Görsel Yükleme Yöntemi:",
        ["📱 Telefon / Web Kamerasından Çek", "📁 Galeriden / Dosyadan Seç", "📝 Sadece Kalemleri Manuel Gir"],
        horizontal=True
    )

    if input_method == "📱 Telefon / Web Kamerasından Çek":
        cam_file = st.camera_input("Kamerayı kasa fişine doğru tutun ve çekin:")
        if cam_file:
            receipt_image_bytes = cam_file.getvalue()
            receipt_filename = f"cam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            st.success("✅ Fotoğraf başarıyla yakalandı!")
    elif input_method == "📁 Galeriden / Dosyadan Seç":
        gal_file = st.file_uploader("Kasa Fişi Fotoğrafı Seçin:", type=["png", "jpg", "jpeg", "webp"], key="tab_gal_file")
        if gal_file:
            receipt_image_bytes = gal_file.getvalue()
            receipt_filename = gal_file.name
            st.image(gal_file, caption=f"Yüklenen: {gal_file.name}", width=260)
            st.success("✅ Görsel seçildi!")

    st.markdown("---")
    st.markdown("### 1️⃣ Fiş Bilgileri")

    m_c1, m_c2, m_c3, m_c4 = st.columns(4)
    with m_c1:
        f_date = st.date_input("Fiş Tarihi:", datetime.now())
    with m_c2:
        f_market = st.selectbox("Market:", ["PENNY", "HIT", "EDEKA", "ALDI SÜD", "dm", "tegut...", "Wolt Market", "Diğer"])
    with m_c3:
        f_receipt_no = st.text_input("Fiş No (Beleg):", placeholder="Örn: 5573").strip()
    with m_c4:
        f_payer = st.selectbox("Kim Ödedi?:", ["Ortak", "Ben", "Kız Arkadaşım"])

    # ⚠️ Real-time Duplicate Receipt Detection
    is_duplicate = False
    if f_receipt_no:
        existing_matches = df[
            (df["fis_no"].astype(str) == str(f_receipt_no)) &
            (df["market"].str.lower() == f_market.lower())
        ]
        if not existing_matches.empty:
            is_duplicate = True
            e_total = existing_matches["toplam_fiyat"].sum()
            e_date = existing_matches["tarih"].iloc[0]
            st.warning(f"⚠️ **DİKKAT: BU FİŞİ DAHA ÖNCE ZATEN YÜKLEDİNİZ!**\n\n{e_date} tarihli **{f_market} (Fiş #{f_receipt_no})** daha önce **{len(existing_matches)} ürün** ile (toplam **€{e_total:.2f}**) sisteme kaydedilmiş!")
            allow_duplicate = st.checkbox("Yine de mükerrer (çift) olarak kaydetmek istiyorum", value=False)
        else:
            allow_duplicate = True
    else:
        allow_duplicate = True

    st.markdown("---")
    st.markdown("### 2️⃣ Fişteki Ürün Kalemleri")
    st.caption("Ürünleri tabloya satır olarak yazabilir, '+' butonuna basarak yeni satır ekleyebilirsiniz.")

    # Initialize editable dataframe session state
    if "receipt_editor_data" not in st.session_state:
        st.session_state.receipt_editor_data = pd.DataFrame([
            {"Ürün Adı": "", "Miktar": 1.0, "Birim Fiyat (€)": 0.0, "KDV": "B (7%)"},
            {"Ürün Adı": "", "Miktar": 1.0, "Birim Fiyat (€)": 0.0, "KDV": "B (7%)"},
            {"Ürün Adı": "", "Miktar": 1.0, "Birim Fiyat (€)": 0.0, "KDV": "B (7%)"}
        ])

    edited_df = st.data_editor(
        st.session_state.receipt_editor_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Ürün Adı": st.column_config.TextColumn("Ürün Adı (Örn: Dana Kıyma, Muz)", required=True),
            "Miktar": st.column_config.NumberColumn("Miktar", min_value=0.01, default=1.0, step=0.1, format="%.2f"),
            "Birim Fiyat (€)": st.column_config.NumberColumn("Birim Fiyat (€)", min_value=0.0, default=0.0, step=0.1, format="€%.2f"),
            "KDV": st.column_config.SelectboxColumn("KDV", options=["B (7%)", "A (19%)", "C (7%)"], default="B (7%)")
        }
    )

    # Calculate Total
    valid_items = edited_df[edited_df["Ürün Adı"].astype(str).str.strip() != ""]
    calculated_sum = (valid_items["Miktar"] * valid_items["Birim Fiyat (€)"]).sum() if not valid_items.empty else 0.0

    st.markdown(f"#### 💰 Fiş Toplamı: <strong style='color:#10b981; font-size:1.3rem;'>€{calculated_sum:,.2f}</strong> ({len(valid_items)} ürün)", unsafe_allow_html=True)

    # 💾 SAVE BUTTON
    if st.button("💾 FİŞİ VE ÜRÜNLERİ SİSTEME KAYDET", type="primary", use_container_width=True):
        if valid_items.empty:
            st.error("Lütfen en az bir ürün adı ve fiyatı girin!")
        elif is_duplicate and not allow_duplicate:
            st.error("⚠️ Mükerrer fiş kaydı engellendi! Aynı fişi iki kez kaydetmemek için lütfen kontrol edin veya 'Yine de kaydet' kutusunu işaretleyin.")
        else:
            # Save Image if provided
            saved_image_rel_path = None
            if receipt_image_bytes:
                img_ext = os.path.splitext(receipt_filename)[1] if receipt_filename else ".jpg"
                img_name = f"receipt_{f_date}_{f_receipt_no or datetime.now().strftime('%H%M%S')}{img_ext}"
                full_img_path = os.path.join(RECEIPTS_DIR, img_name)
                with open(full_img_path, "wb") as f_img:
                    f_img.write(receipt_image_bytes)
                saved_image_rel_path = f"/receipts/{img_name}"

            # Ingest Items
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                all_current_items = json.load(f)

            max_id = max([it.get("id", 0) for it in all_current_items]) if all_current_items else 0
            new_added = 0

            for _, row in valid_items.iterrows():
                max_id += 1
                raw_u = str(row["Ürün Adı"]).strip()
                can_name, m_cat = normalize_product(raw_u)
                q_val = float(row.get("Miktar", 1.0))
                p_val = float(row.get("Birim Fiyat (€)", 0.0))
                tot_val = round(q_val * p_val, 2)
                kdv_val = str(row.get("KDV", "B (7%)"))

                new_item_dict = {
                    "id": max_id,
                    "tarih": str(f_date),
                    "market": f_market,
                    "urun": raw_u,
                    "kanonik_urun": can_name,
                    "marka": f_market,
                    "kategori": m_cat,
                    "alt_kategori": m_cat,
                    "miktar": q_val,
                    "birim_fiyat": p_val,
                    "toplam_fiyat": tot_val,
                    "kdv": kdv_val,
                    "fis_no": f_receipt_no,
                    "fis_resmi": saved_image_rel_path,
                    "odeyen": f_payer
                }
                all_current_items.insert(0, new_item_dict)
                new_added += 1

            save_items_to_db(all_current_items)
            st.session_state.pop("uploaded_receipt_bytes", None)
            st.session_state.pop("uploaded_receipt_name", None)
            st.session_state.receipt_editor_data = pd.DataFrame([
                {"Ürün Adı": "", "Miktar": 1.0, "Birim Fiyat (€)": 0.0, "KDV": "B (7%)"},
                {"Ürün Adı": "", "Miktar": 1.0, "Birim Fiyat (€)": 0.0, "KDV": "B (7%)"}
            ])
            st.success(f"🎉 Harika! {new_added} ürün ve fiş başarıyla veritabanına kaydedildi. Grafikler ve bütçe güncelleniyor...")
            st.rerun()

# ========================================================
# DETAILED DATA TABLE & EXPORT
# ========================================================
st.markdown("---")
st.subheader("📋 Tüm Alışveriş Kalemleri Tablosu")

t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.caption(f"Filtrelenen: {len(filtered_df)} kayıt (Toplam {len(df)} üründen)")
with t_col2:
    csv_bytes = filtered_df.to_csv(index=False, sep=";").encode("utf-8-sig")
    st.download_button(
        label="📥 Excel / CSV Olarak İndir",
        data=csv_bytes,
        file_name="Bizim_Market_Alisverisleri_Munih.csv",
        mime="text/csv",
        use_container_width=True
    )

display_cols = ["tarih", "market", "kanonik_urun", "urun", "marka", "kategori", "miktar", "birim_fiyat", "toplam_fiyat", "kdv", "fis_no", "odeyen"]
st.dataframe(
    filtered_df[display_cols].sort_values(by="tarih", ascending=False),
    use_container_width=True,
    column_config={
        "tarih": "Tarih",
        "market": "Market",
        "kanonik_urun": "Standart Ürün",
        "urun": "Fişteki Adı",
        "marka": "Marka",
        "kategori": "Kategori",
        "miktar": st.column_config.NumberColumn("Miktar", format="%.2f"),
        "birim_fiyat": st.column_config.NumberColumn("Birim Fiyat", format="€%.2f"),
        "toplam_fiyat": st.column_config.NumberColumn("Toplam", format="€%.2f"),
        "kdv": "KDV",
        "fis_no": "Fiş No",
        "odeyen": "Ödeyen"
    }
)
