# -*- coding: utf-8 -*-
"""
💑 Bizim Market Paneli – Streamlit Versiyonu
Çalıştırmak için:
    pip install streamlit pandas plotly openpyxl
    streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Bizim Market Paneli 💑",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
</style>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "market_data.json")

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            df["tarih"] = pd.to_datetime(df["tarih"])
            return df
    return pd.DataFrame()

df = load_data()

# Header
st.title("💑 Bizim Market Paneli – München")
st.caption("Birlikte Ortak Market Harcaması, Fiş Takibi & Enflasyon Analitiği")

if df.empty:
    st.warning("Henüz veri bulunamadı.")
    st.stop()

# Sidebar Filters & Receipt Upload
with st.sidebar:
    st.header("📸 Fiş / Veri Yükle")
    uploaded_file = st.file_uploader("Yeni Fiş Fotoğrafı veya Excel Yükle", type=["png", "jpg", "jpeg", "xlsx", "csv"])
    if uploaded_file:
        st.success(f"Yüklendi: {uploaded_file.name}")
        st.info("Fiş analizi ve veri eşleştirmesi web panelinde canlı olarak da desteklenmektedir.")

    st.markdown("---")
    st.header("🔍 Filtreler")
    
    # Store filter
    stores = ["Tümü"] + sorted(list(df["market"].unique()))
    selected_store = st.selectbox("Market Seç", stores)

    # Category filter
    categories = ["Tümü"] + sorted(list(df["kategori"].dropna().unique()))
    selected_cat = st.selectbox("Kategori Seç", categories)

    # Payer filter
    payers = ["Tümü"] + sorted(list(df["odeyen"].dropna().unique()))
    selected_payer = st.selectbox("Kim Ödedi?", payers)

# Apply filters
filtered_df = df.copy()
if selected_store != "Tümü":
    filtered_df = filtered_df[filtered_df["market"] == selected_store]
if selected_cat != "Tümü":
    filtered_df = filtered_df[filtered_df["kategori"] == selected_cat]
if selected_payer != "Tümü":
    filtered_df = filtered_df[filtered_df["odeyen"] == selected_payer]

# KPI Metrics
total_spend = filtered_df["toplam_fiyat"].sum()
item_count = len(filtered_df)
receipt_count = filtered_df["fis_no"].nunique()
avg_basket = total_spend / receipt_count if receipt_count > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Harcama", f"€{total_spend:,.2f}")
col2.metric("Toplam Ürün", f"{item_count} adet")
col3.metric("Fiş Sayısı", f"{receipt_count} fiş")
col4.metric("Ortalama Fiş", f"€{avg_basket:,.2f}")

st.markdown("---")

# Charts Row 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("📅 Zaman İçinde Harcama")
    daily_spend = filtered_df.groupby("tarih")["toplam_fiyat"].sum().reset_index()
    fig_time = px.area(daily_spend, x="tarih", y="toplam_fiyat", 
                       labels={"toplam_fiyat": "Tutar (€)", "tarih": "Tarih"},
                       color_discrete_sequence=["#10b981"])
    fig_time.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
    st.plotly_chart(fig_time, use_container_width=True)

with c2:
    st.subheader("🏪 Market Payları")
    market_spend = filtered_df.groupby("market")["toplam_fiyat"].sum().reset_index()
    fig_market = px.pie(market_spend, names="market", values="toplam_fiyat",
                        color="market",
                        color_discrete_map={
                            "PENNY": "#cf0820", "HIT": "#e30613", "EDEKA": "#005ca9",
                            "ALDI SÜD": "#002069", "dm": "#7b2b82", "tegut...": "#d97706",
                            "Wolt Market": "#06b6d4"
                        }, hole=0.5)
    fig_market.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
    st.plotly_chart(fig_market, use_container_width=True)

# Charts Row 2
c3, c4 = st.columns(2)

with c3:
    st.subheader("📦 Kategori Harcamaları")
    cat_spend = filtered_df.groupby("kategori")["toplam_fiyat"].sum().sort_values(ascending=True).tail(8).reset_index()
    fig_cat = px.bar(cat_spend, x="toplam_fiyat", y="kategori", orientation="h",
                     labels={"toplam_fiyat": "Tutar (€)", "kategori": ""},
                     color_discrete_sequence=["#8b5cf6"])
    fig_cat.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320)
    st.plotly_chart(fig_cat, use_container_width=True)

with c4:
    st.subheader("🥩 Akıllı Fiyat Karşılaştırması (Kanonik Eşleşme)")
    canonical_list = sorted(list(df["kanonik_urun"].dropna().unique()))
    comp_product = st.selectbox("Karşılaştırılacak Ürün:", canonical_list)
    sub_df = df[df["kanonik_urun"] == comp_product]
    if not sub_df.empty:
        fig_comp = px.scatter(sub_df, x="tarih", y="birim_fiyat", color="market", size="toplam_fiyat",
                              labels={"birim_fiyat": "Birim Fiyat (€)", "tarih": "Tarih"},
                              hover_data=["urun", "kanonik_urun", "market"])
        fig_comp.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=280)
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Bu ürün için eşleşme bulunamadı.")

# Detailed Data Table
st.markdown("---")
st.subheader("📋 Alışveriş Kalemleri Tablosu")
display_cols = ["tarih", "market", "kanonik_urun", "urun", "marka", "kategori", "miktar", "birim_fiyat", "toplam_fiyat", "kdv", "fis_no", "odeyen"]
st.dataframe(filtered_df[display_cols].sort_values(by="tarih", ascending=False), use_container_width=True)
