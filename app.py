import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Ekonomi Hutan Kalimantan Selatan",
    layout="wide"
)

st.title("🌳 Ekonomi Hutan Kalimantan Selatan")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Beranda",
        "Kalkulator TEV",
        "Analisis Trade-off",
        "Kebijakan PES",
        "Studi Kasus"
    ]
)

# =========================
# BERANDA
# =========================

if menu == "Beranda":

    st.header("Profil Hutan Kalimantan Selatan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Flora", "3.000 Spesies")
    col2.metric("Fauna", "500 Spesies")
    col3.metric("Cadangan Karbon", "172 Juta Ton")
    col4.metric("Wisata Alam", "12 Lokasi")

    st.subheader("Jenis Tanaman Dominan")

    tanaman = pd.DataFrame({
        "Tanaman": [
            "Ulin",
            "Meranti",
            "Keruing",
            "Bangkirai",
            "Kapur"
        ]
    })

    st.dataframe(tanaman)

    st.subheader("Komposisi Jenis Tegakan")

    tegakan = pd.DataFrame({
        "Jenis Tegakan": [
            "Hutan Primer",
            "Hutan Sekunder",
            "Hutan Pegunungan",
            "Hutan Mangrove",
            "Hutan Rawa"
        ],
        "Persentase": [15,45,20,10,10]
    })

    fig = px.pie(
        tegakan,
        names="Jenis Tegakan",
        values="Persentase"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TEV
# =========================

elif menu == "Kalkulator TEV":

    st.header("Kalkulator Total Economic Value (TEV)")

    luas = st.number_input(
        "Luas Hutan (ha)",
        min_value=0.0,
        value=100000.0
    )

    flora = st.number_input(
        "Jumlah Flora",
        min_value=0,
        value=3000
    )

    fauna = st.number_input(
        "Jumlah Fauna",
        min_value=0,
        value=500
    )

    karbon = st.number_input(
        "Cadangan Karbon (ton)",
        min_value=0.0,
        value=172000000.0
    )

    wisata = st.number_input(
        "Jumlah Objek Wisata",
        min_value=0,
        value=12
    )

    if st.button("Hitung TEV"):

        direct_use = luas * 0.00025
        environmental = luas * 0.00045
        option_value = luas * 0.00015
        existence_value = luas * 0.00015

        total_tev = (
            direct_use +
            environmental +
            option_value +
            existence_value
        )

        hasil = pd.DataFrame({
            "Komponen": [
                "Nilai Guna Langsung",
                "Nilai Pengaturan Lingkungan",
                "Nilai Pilihan",
                "Nilai Eksistensi"
            ],
            "Nilai": [
                direct_use,
                environmental,
                option_value,
                existence_value
            ]
        })

        st.dataframe(hasil)

        st.success(
            f"Total Economic Value (TEV): Rp {total_tev:.2f} Miliar/Tahun"
        )

        fig = px.pie(
            hasil,
            names="Komponen",
            values="Nilai"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================
# TRADE OFF
# =========================

elif menu == "Analisis Trade-off":

    st.header("Analisis Trade-off Pemanfaatan Hutan")

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
        "Skenario hutan lestari memberikan nilai ekonomi total yang lebih tinggi dibandingkan konversi lahan maupun eksploitasi kayu."
    )

# =========================
# PES
# =========================

elif menu == "Kebijakan PES":

    st.header("Payment for Ecosystem Services (PES)")

    harga_karbon = st.number_input(
        "Harga Karbon (Rp/Ton)",
        value=150000
    )

    karbon = st.number_input(
        "Cadangan Karbon (Ton)",
        value=172000000
    )

    if st.button("Hitung PES"):

        pes = harga_karbon * karbon

        st.success(
            f"Potensi Pendapatan PES: Rp {pes:,.0f}"
        )

# =========================
# STUDI KASUS
# =========================

elif menu == "Studi Kasus":

    st.header("Studi Kasus Hutan Kalimantan Selatan")

    lokasi = st.selectbox(
        "Pilih Lokasi",
        [
            "Pegunungan Meratus",
            "Loksado",
            "Tahura Sultan Adam",
            "Pulau Kembang"
        ]
    )

    data = {
        "Pegunungan Meratus": {
            "Biodiversitas": "Tinggi",
            "Karbon": "Sangat Tinggi",
            "Wisata": "Ekowisata"
        },
        "Loksado": {
            "Biodiversitas": "Tinggi",
            "Karbon": "Tinggi",
            "Wisata": "Bamboo Rafting"
        },
        "Tahura Sultan Adam": {
            "Biodiversitas": "Sedang",
            "Karbon": "Tinggi",
            "Wisata": "Wisata Alam"
        },
        "Pulau Kembang": {
            "Biodiversitas": "Sedang",
            "Karbon": "Sedang",
            "Wisata": "Konservasi Satwa"
        }
    }

    st.subheader(lokasi)

    st.write(
        f"Biodiversitas: {data[lokasi]['Biodiversitas']}"
    )

    st.write(
        f"Karbon: {data[lokasi]['Karbon']}"
    )

    st.write(
        f"Potensi Wisata: {data[lokasi]['Wisata']}"
    )
