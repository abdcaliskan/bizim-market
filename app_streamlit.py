# -*- coding: utf-8 -*-
"""
💑 Bizim Market Paneli – Streamlit Versiyonu (München 🥨)
Ortak Market Harcaması, Fiş Takibi, Fiyat Kıyaslama & Enflasyon Analitiği
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
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
        padding: 16px 20px;
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
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    
    /* Budget Bar Container */
    .budget-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }

    /* Price radar badge */
    .radar-box {
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Path to Data File
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "market_data.json")
RECEIPTS_DIR = os.path.join(os.path.dirname(__file__), "public", "receipts")

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

# Load Data
@st.cache_data(ttl=5)
def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            df["tarih_dt"] = pd.to_datetime(df["tarih"])
            # Ensure canonical column exists
            if "kanonik_urun" not in df.columns:
                df["kanonik_urun"] = df["urun"]
            return df
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Veritabanı dosyası bulunamadı!")
    st.stop()

# Helper: Save Data
def save_data(updated_items):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(updated_items, f, ensure_ascii=False, indent=2)
    st.cache_data.clear()

# ========================================================
# SIDEBAR: FILTERS & QUICK CONTROLS
# ========================================================
with st.sidebar:
    st.markdown("### 💑 Bizim Market")
    st.caption("München Alışveriş & Fiş Takip Paneli")
    st.markdown("---")

    st.subheader("🔍 Filtreler")

    # Date Range Filter
    date_preset = st.radio(
        "Zaman Aralığı:",
        ["Tümü", "Bu Ay (Ekim 2026)", "Geçen Ay (Eylül 2026)", "Son 7 Gün"],
        index=0
    )

    # Store Filter
    all_stores = ["Tümü"] + sorted(list(df["market"].dropna().unique()))
    selected_store = st.selectbox("🏪 Market:", all_stores)

    # Category Filter
    all_cats = ["Tümü"] + sorted(list(df["kategori"].dropna().unique()))
    selected_cat = st.selectbox("📦 Kategori:", all_cats)

    # Payer Filter
    all_payers = ["Tümü"] + sorted(list(df["odeyen"].dropna().unique()))
    selected_payer = st.selectbox("👤 Kim Ödedi?:", all_payers)

    # Search Box
    search_query = st.text_input("🔎 Ürün veya Marka Ara:", placeholder="Örn: kıyma, yumurta, süt...").strip().lower()

    st.markdown("---")
    st.markdown("### ⚙️ Aylık Bütçe Hedefi")
    budget_goal = st.number_input("Hedef Bütçe (€):", min_value=100.0, max_value=2000.0, value=450.0, step=25.0)

# Filter Dataframe
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

# October Spend & Budget Calculation
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
# KPI METRICS ROW
# ========================================================
total_spend = filtered_df["toplam_fiyat"].sum()
total_items = len(filtered_df)
receipt_count = filtered_df["fis_no"].replace("", pd.NA).dropna().nunique()
avg_basket = total_spend / receipt_count if receipt_count > 0 else 0

# Pfand Balance
pfand_df = filtered_df[
    filtered_df["kategori"].str.lower().str.contains("depozito", na=False) |
    filtered_df["urun"].str.lower().str.contains("pfand", na=False)
]
pfand_net = pfand_df["toplam_fiyat"].sum()

# Top Store
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
tab_overview, tab_stores, tab_radar, tab_gallery, tab_add = st.tabs([
    "📊 Genel Bakış & Trendler",
    "🏪 Market & Kategori Dağılımı",
    "🥩 Akıllı Fiyat Radarı (Kıyaslama)",
    "🖼️ Orijinal Fiş Galerisi",
    "➕ Yeni Fiş / Ürün Ekle"
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
        # Daily bar
        fig_trend.add_trace(go.Bar(
            x=daily_df["tarih_dt"],
            y=daily_df["toplam_fiyat"],
            name="Günlük Harcama (€)",
            marker_color="#10b981",
            opacity=0.85
        ))
        # Cumulative line
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

    # Spending by Payer (Kim Ödedi?)
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

    # Market x Category Cross-Analysis
    st.subheader("📊 Market & Kategori Çapraz Harcama Tablosu")
    pivot_df = filtered_df.pivot_table(index="market", columns="kategori", values="toplam_fiyat", aggfunc="sum", fill_value=0)
    st.dataframe(pivot_df.style.format("€{:.2f}").background_gradient(cmap="Blues", axis=None), use_container_width=True)

# --------------------------------------------------------
# TAB 3: AKILLI FİYAT RADARI (KIYASLAMA & ENFLASYON)
# --------------------------------------------------------
with tab_radar:
    st.subheader("🔍 Akıllı Ürün Fiyat Radarı & Karşılaştırma")
    st.caption("Gramaj farkları ve kasa isimleri filtrelenerek ürünlerin marketler arası fiyat farkı kıyaslanır.")

    # Canonical products that have multiple purchases
    popular_staples = [
        "Dana Kıyma",
        "Tavuk / Hindi Göğüs Fileto",
        "Yumurta (10'lu)",
        "Yulaf Sütü Barista",
        "Muz",
        "Tereyağı (Kerrygold)",
        "Patates Cipsi",
        "Beyaz Peynir (Mitakos)",
        "Emmental Peyniri",
        "Yunan Yoğurdu",
        "Nutella / Fındık Kreması",
        "Makarna",
        "Dondurulmuş Pizza",
        "Ayran",
        "Kapsül Kahve",
        "Salatalık",
        "Havuç"
    ]
    # Also add any other canonical items in dataset
    all_canonicals = sorted(list(set(popular_staples + list(df["kanonik_urun"].dropna().unique()))))

    selected_product = st.selectbox("🎯 Karşılaştırılacak Ürünü Seçin:", all_canonicals, index=0)

    # Matching items
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

        # Radar Cards
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

        # Timeline Scatter/Line of Purchases
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

        # History Table
        st.markdown("##### 🧾 Fiyat Geçmişi Detayları:")
        st.dataframe(
            match_df[["tarih", "market", "kanonik_urun", "urun", "miktar", "birim_fiyat", "toplam_fiyat", "fis_no"]]
            .sort_values("tarih", ascending=False),
            use_container_width=True
        )
    else:
        st.info("Bu ürün için henüz kayıt bulunamadı.")

# --------------------------------------------------------
# TAB 4: ORİJİNAL FİŞ GALERİSİ
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
# TAB 5: YENİ FİŞ / ÜRÜN EKLE
# --------------------------------------------------------
with tab_add:
    st.subheader("➕ Yeni Fiş veya Ürün Girişi")
    st.caption("Fiş fotoğrafını yükleyebilir veya yeni ürün kalemlerini ekleyebilirsiniz.")

    with st.expander("📸 Fiş Fotoğrafı Yükle & Arşivle", expanded=True):
        up_file = st.file_uploader("Fiş Görseli Seç (PNG / JPG / WEBP):", type=["png", "jpg", "jpeg", "webp"])
        if up_file:
            st.image(up_file, caption=f"Yüklenen: {up_file.name}", width=250)
            st.success("Fiş fotoğrafı başarıyla yüklendi!")

    st.markdown("#### 📝 Yeni Ürün Kalemi Ekle")
    with st.form("add_item_form", clear_on_submit=True):
        f_c1, f_c2, f_c3 = st.columns(3)
        with f_c1:
            form_date = st.date_input("Tarih:", datetime.now())
            form_market = st.selectbox("Market:", ["PENNY", "HIT", "EDEKA", "ALDI SÜD", "dm", "tegut...", "Wolt Market", "Diğer"])
        with f_c2:
            form_urun = st.text_input("Ürün Adı:", placeholder="Örn: Dana Kıyma, Tavuk Göğsü, Yoğurt")
            form_brand = st.text_input("Marka (Opsiyonel):", placeholder="Örn: Penny, Körfez, Delverde")
        with f_c3:
            form_cat = st.selectbox("Kategori:", [
                "Et, Tavuk & Şarküteri", "Meyve & Sebze", "Süt, Peynir & Yumurta",
                "Fırın & Ekmek", "Temel Gıda & Makarna", "Konserve, Sos & Baharat",
                "Kahvaltılık", "Atıştırmalık & Tatlı", "İçecekler",
                "Dondurulmuş & Hazır Yemek", "Ev & Temizlik", "Kişisel Bakım", "Depozito", "Diğer"
            ])
            form_payer = st.selectbox("Kim Ödedi?:", ["Ortak", "Ben", "Kız Arkadaşım"])

        f_q1, f_q2, f_q3, f_q4 = st.columns(4)
        with f_q1:
            form_qty = st.number_input("Miktar:", min_value=0.01, value=1.0, step=1.0)
        with f_q2:
            form_unit = st.number_input("Birim Fiyat (€):", min_value=0.0, value=1.99, step=0.1)
        with f_q3:
            form_total = st.number_input("Toplam Tutar (€):", value=round(form_qty * form_unit, 2), step=0.1)
        with f_q4:
            form_receipt_no = st.text_input("Fiş No (Beleg):", placeholder="Örn: 5573")

        # Duplicate Warning Check
        if form_receipt_no:
            existing_match = df[
                (df["fis_no"] == form_receipt_no) & 
                (df["market"] == form_market)
            ]
            if not existing_match.empty:
                st.warning(f"⚠️ DİKKAT: Bu fiş numarası (#{form_receipt_no}) daha önce {len(existing_match)} kalem ürün ile sisteme kaydedilmiş! Mükerrer kayıt yapmadığınızdan emin olun.")

        submit_btn = st.form_submit_button("✅ Ürünü Veritabanına Ekle", use_container_width=True)

        if submit_btn and form_urun:
            new_id = int(df["id"].max()) + 1 if "id" in df.columns and not df.empty else 1
            new_entry = {
                "id": new_id,
                "tarih": str(form_date),
                "market": form_market,
                "urun": form_urun,
                "kanonik_urun": form_urun,
                "marka": form_brand,
                "kategori": form_cat,
                "miktar": float(form_qty),
                "birim_fiyat": float(form_unit),
                "toplam_fiyat": float(form_total),
                "kdv": "B (7%)",
                "fis_no": form_receipt_no,
                "odeyen": form_payer
            }
            # Append and save
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                current_list = json.load(f)
            current_list.insert(0, new_entry)
            save_data(current_list)
            st.success(f"🎉 '{form_urun}' başarıyla kaydedildi!")
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
    # CSV Download Button
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
