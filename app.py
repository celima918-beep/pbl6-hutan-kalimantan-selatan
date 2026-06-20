import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# =====================
# KONFIGURASI HALAMAN
# =====================

st.set_page_config(
    page_title="Ekonomi Hutan Kalimantan Selatan",
    layout="wide"
)

# =====================
# LOGO
# =====================

logo = Image.open("logo.png")

col1, col2 = st.columns([1,5])

with col1:
    st.image(logo, width=120)

with col2:
    st.title("Ekonomi Hutan Kalimantan Selatan")
    st.write("Project Based Learning Ekonomi Sumber Daya Alam dan Lingkungan")

st.divider()

# =====================
# SIDEBAR
# =====================

st.sidebar.image(logo, width=150)

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Beranda",
        "Biodiversitas",
        "Fungsi Hutan",
        "Karbon",
        "Wisata Alam",
        "Kalkulator TEV",
        "Analisis Trade-Off",
        "PES"
    ]
)

# =====================
# BERANDA
# =====================

if menu == "Beranda":

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Flora", "3.000")
    col2.metric("Fauna", "500")
    col3.metric("Karbon", "172 Juta Ton")
    col4.metric("Wisata", "12 Lokasi")

    st.write("Dashboard Ekonomi Hutan Kalimantan Selatan")

# =====================
# BIODIVERSITAS
# =====================

elif menu == "Biodiversitas":

    data = pd.DataFrame({
        "Kategori": ["Flora", "Fauna"],
        "Jumlah": [3000, 500]
    })

    st.dataframe(data)

    fig = px.bar(
        data,
        x="Kategori",
        y="Jumlah"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# FUNGSI HUTAN
# =====================

elif menu == "Fungsi Hutan":

    st.subheader("Fungsi Hutan")

    fungsi = [
        "Penyerap Karbon",
        "Pengatur Tata Air",
        "Pencegah Erosi",
        "Habitat Satwa",
        "Wisata Alam"
    ]

    for item in fungsi:
        st.write("•", item)

# =====================
# KARBON
# =====================

elif menu == "Karbon":

    karbon = pd.DataFrame({
        "Kategori": [
            "Cadangan Karbon",
            "Serapan Karbon Tahunan"
        ],
        "Nilai": [
            172000000,
            6400000
        ]
    })

    st.dataframe(karbon)

    fig = px.pie(
        karbon,
        names="Kategori",
        values="Nilai"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# WISATA
# =====================

elif menu == "Wisata Alam":

    wisata = pd.DataFrame({
        "Destinasi": [
            "Loksado",
            "Tahura Sultan Adam",
            "Pegunungan Meratus",
            "Air Terjun Haratai",
            "Pulau Kembang"
        ]
    })

    st.dataframe(wisata)

# =====================
# TEV
# =====================

elif menu == "Kalkulator TEV":

    luas = st.number_input(
        "Luas Hutan (ha)",
        value=100000
    )

    tev = luas * 950000

    st.metric(
        "Total Economic Value",
        f"Rp {tev:,.0f}"
    )

# =====================
# TRADE OFF
# =====================

elif menu == "Analisis Trade-Off":

    tradeoff = pd.DataFrame({
        "Skenario": [
            "Hutan Lestari",
            "Konversi Sawit",
            "Eksploitasi Kayu"
        ],
        "Nilai": [
            95,
            65,
            40
        ]
    })

    fig = px.bar(
        tradeoff,
        x="Nilai",
        y="Skenario",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# PES
# =====================

elif menu == "PES":

    karbon = st.number_input(
        "Cadangan Karbon (Ton)",
        value=172000000
    )

    harga = st.number_input(
        "Harga Karbon (Rp/Ton)",
        value=150000
    )

    hasil = karbon * harga

    st.metric(
        "Potensi Pendapatan PES",
        f"Rp {hasil:,.0f}"
    )
