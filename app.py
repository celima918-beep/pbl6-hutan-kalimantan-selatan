import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Ekonomi Hutan Kalimantan Selatan",
    page_icon="🌳",
    layout="wide"
)

# =====================
# SIDEBAR
# =====================

st.sidebar.title("🌳 Ekonomi Hutan")

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

    st.title("Ekonomi Hutan Kalimantan Selatan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Flora", "3.000")
    col2.metric("Fauna", "500")
    col3.metric("Karbon", "172 Juta Ton")
    col4.metric("Wisata", "12 Lokasi")

    st.markdown("""
    Aplikasi ini menampilkan informasi ekonomi sumber daya hutan
    Kalimantan Selatan yang meliputi biodiversitas, karbon,
    jasa lingkungan, wisata alam, dan simulasi nilai ekonomi.
    """)

# =====================
# BIODIVERSITAS
# =====================

elif menu == "Biodiversitas":

    st.header("Biodiversitas Hutan Kalimantan Selatan")

    df = pd.DataFrame({
        "Kategori": ["Flora", "Fauna"],
        "Jumlah": [3000, 500]
    })

    st.dataframe(df)

    fig = px.bar(
        df,
        x="Kategori",
        y="Jumlah",
        title="Jumlah Keanekaragaman Hayati"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# FUNGSI HUTAN
# =====================

elif menu == "Fungsi Hutan":

    st.header("Fungsi Hutan")

    fungsi = pd.DataFrame({
        "Fungsi": [
            "Penyerap Karbon",
            "Pengatur Tata Air",
            "Pencegah Erosi",
            "Habitat Satwa",
            "Wisata Alam"
        ]
    })

    st.dataframe(fungsi)

# =====================
# KARBON
# =====================

elif menu == "Karbon":

    st.header("Cadangan Karbon")

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
        values="Nilai",
        title="Distribusi Karbon"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# WISATA ALAM
# =====================

elif menu == "Wisata Alam":

    st.header("Wisata Alam Kalimantan Selatan")

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

    st.header("Kalkulator Total Economic Value")

    luas = st.number_input(
        "Luas Hutan (ha)",
        value=100000
    )

    direct_use = luas * 250000
    indirect_use = luas * 450000
    option_value = luas * 150000
    existence_value = luas * 100000

    total = (
        direct_use +
        indirect_use +
        option_value +
        existence_value
    )

    tev = pd.DataFrame({
        "Komponen": [
            "Direct Use",
            "Indirect Use",
            "Option Value",
            "Existence Value"
        ],
        "Nilai": [
            direct_use,
            indirect_use,
            option_value,
            existence_value
        ]
    })

    st.dataframe(tev)

    st.success(
        f"Total Economic Value = Rp {total:,.0f}"
    )

    fig = px.pie(
        tev,
        names="Komponen",
        values="Nilai"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================
# TRADE OFF
# =====================

elif menu == "Analisis Trade-Off":

    st.header("Analisis Trade-Off")

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

    st.info(
        "Hutan lestari memberikan nilai ekonomi tertinggi."
    )

# =====================
# PES
# =====================

elif menu == "PES":

    st.header("Payment for Ecosystem Services")

    karbon = st.number_input(
        "Cadangan Karbon (Ton)",
        value=172000000
    )

    harga = st.number_input(
        "Harga Karbon (Rp/Ton)",
        value=150000
    )

    pes = karbon * harga

    st.metric(
        "Potensi Pendapatan PES",
        f"Rp {pes:,.0f}"
    )
