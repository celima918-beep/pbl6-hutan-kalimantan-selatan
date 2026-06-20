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
# DATA UTAMA DEFAULT (BPS KALSEL)
# =====================

@st.cache_data
def load_data_kehutanan():
    data_kab = {
        "Kabupaten/Kota": [
            "Tanah Laut", "Kota Baru", "Banjar", "Barito Kuala", "Tapin", 
            "Hulu Sungai Selatan", "Hulu Sungai Tengah", "Hulu Sungai Utara", 
            "Tabalong", "Tanah Bumbu", "Balangan", "Kota Banjarmasin", "Kota Banjar Baru"
        ],
        "Hutan Lindung (ha)": [13688.39, 149531.40, 44856.83, 144.90, 10150.96, 23484.74, 40788.41, 0.00, 75886.95, 86950.65, 60429.88, 0.00, 1330.21],
        "Suaka Alam & Pelestarian (ha)": [27338.06, 83078.47, 97084.76, 3666.69, 0.00, 249.34, 0.00, 0.00, 0.00, 5475.52, 0.00, 0.00, 0.00],
        "Hutan Produksi Terbatas (ha)": [5235.57, 881.23, 25103.68, 0.00, 841.51, 0.00, 14006.59, 0.00, 52827.91, 25038.93, 5.70, 0.00, 0.00],
        "Hutan Produksi Tetap (ha)": [70157.61, 241902.40, 82503.74, 0.00, 5840.76, 11250.48, 8895.13, 16204.05, 90059.52, 134348.78, 24100.78, 0.00, 0.00],
        "Hutan Produksi Konversi (ha)": [8788.74, 26960.68, 2037.31, 876.66, 6738.37, 18587.09, 0.00, 25861.33, 3697.69, 25732.33, 0.00, 0.00, 0.00]
    }
    df = pd.DataFrame(data_kab)
    df["Total Kawasan Hutan (ha)"] = df.iloc[:, 1:6].sum(axis=1)
    return df

df_hutan = load_data_kehutanan()

total_lindung = df_hutan["Hutan Lindung (ha)"].sum()
total_suaka = df_hutan["Suaka Alam & Pelestarian (ha)"].sum()
total_hpt = df_hutan["Hutan Produksi Terbatas (ha)"].sum()
total_hp = df_hutan["Hutan Produksi Tetap (ha)"].sum()
total_hpk = df_hutan["Hutan Produksi Konversi (ha)"].sum()
total_luas_provinsi = df_hutan["Total Kawasan Hutan (ha)"].sum()

# =====================
# LOGO & HEADER
# =====================

try:
    logo = Image.open("logo.png")
    has_logo = True
except:
    has_logo = False

col1, col2 = st.columns([1,5])

with col1:
    if has_logo:
        st.image(logo, width=120)
    else:
        st.warning("Logo tidak ditemukan")

with col2:
    st.title("Ekonomi Hutan Kalimantan Selatan")
    st.write("Project Based Learning Ekonomi Sumber Daya Alam dan Lingkungan")

st.divider()

# =====================
# SIDEBAR NAVIGATION
# =====================

if has_logo:
    st.sidebar.image(logo, width=150)

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Beranda",
        "Fungsi Hutan",
        "Profil SDA & Jasa Lingkungan",
        "Kalkulator TEV",
        "Analisis Trade-Off",
        "PES"
    ]
)

# =====================
# BERANDA
# =====================

if menu == "Beranda":
    st.subheader("Kondisi Fisik dan Makro Kehutanan")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Luas Hutan", f"{total_luas_provinsi:,.2f} ha")
    col2.metric("Hutan Lindung Terluas", "Kotabaru")
    col3.metric("Cadangan Karbon", "172 Juta Ton")
    col4.metric("Destinasi Wisata", "5 Lokasi Utama")

    st.write("Dashboard ini menyajikan data spasial dan valuasi ekonomi kehutanan Kalimantan Selatan.")
    st.dataframe(df_hutan.drop(columns=["Total Kawasan Hutan (ha)"]), use_container_width=True)

# =====================
# FUNGSI HUTAN
# =====================

elif menu == "Fungsi Hutan":
    st.subheader("Distribusi Luas Lahan Berdasarkan Fungsi Kawasan Hutan Provinsi")
    
    df_fungsi_total = pd.DataFrame({
        "Fungsi Hutan": ["Hutan Lindung", "Suaka Alam & Pelestarian", "Produksi Terbatas", "Produksi Tetap", "Produksi Konversi"],
        "Luas (ha)": [total_lindung, total_suaka, total_hpt, total_hp, total_hpk]
    })
    
    fig_fungsi = px.pie(
        df_fungsi_total, 
        values="Luas (ha)", 
        names="Fungsi Hutan", 
        title="Persentase Pembagian Kawasan Hutan Provinsi"
    )
    st.plotly_chart(fig_fungsi, use_container_width=True)
    st.dataframe(df_fungsi_total, use_container_width=True)

# =====================
# PROFIL SDA & JASA LINGKUNGAN
# =====================

elif menu == "Profil SDA & Jasa Lingkungan":
    st.header("Profil Sumber Daya Alam dan Jasa Lingkungan")
    st.write("Potensi kekayaan hayati, kapasitas karbon, dan objek wisata alam hutan Kalimantan Selatan.")
    st.divider()
    
    st.subheader("1. Keanekaragaman Hayati (Biodiversitas)")
    col_bio1, col_bio2 = st.columns([1, 2])
    
    with col_bio1:
        data_bio = pd.DataFrame({
            "Kategori": ["Flora", "Fauna"],
            "Jumlah Kerapatan Spesies": [3000, 500]
        })
        st.dataframe(data_bio, use_container_width=True)
        
    with col_bio2:
        fig_bio = px.bar(data_bio, x="Kategori", y="Jumlah Kerapatan Spesies", title="Perbandingan Kerapatan Spesies Kehutanan")
        st.plotly_chart(fig_bio, use_container_width=True)
        
    st.divider()
    
    st.subheader("2. Kapasitas Volumetrik Cadangan Karbon")
    col_kar1, col_kar2 = st.columns([1, 2])
    
    with col_kar1:
        data_karbon = pd.DataFrame({
            "Kategori Parameter": ["Cadangan Karbon Tetap", "Serapan Karbon Tahunan"],
            "Volume (Ton)": [172000000, 6400000]
        })
        st.dataframe(data_karbon, use_container_width=True)
        
    with col_kar2:
        fig_karbon = px.pie(data_karbon, names="Kategori Parameter", values="Volume (Ton)", title="Proporsi Distribusi Aspek Karbon")
        st.plotly_chart(fig_karbon, use_container_width=True)
        
    st.divider()
    
    st.subheader("3. Jasa Lingkungan Wisata Rekreasi Alam")
    data_wisata = pd.DataFrame({
        "Destinasi": ["Loksado", "Tahura Sultan Adam", "Pegunungan Meratus", "Air Terjun Haratai", "Pulau Kembang"],
        "Kawasan Administratif": ["Hulu Sungai Selatan", "Banjar/Banjarbaru", "Hulu Sungai Tengah", "Hulu Sungai Selatan", "Barito Kuala"]
    })
    st.dataframe(data_wisata, use_container_width=True)

# =====================
# KALKULATOR TEV
# =====================

elif menu == "Kalkulator TEV":
    st.header("Kalkulator Total Economic Value (TEV)")
    
    pilihan_wilayah = st.selectbox("Pilih Wilayah Analisis:", ["Total Provinsi"] + list(df_hutan["Kabupaten/Kota"]))
    
    if pilihan_wilayah == "Total Provinsi":
        luas_analisis = total_luas_provinsi
    else:
        luas_analisis = df_hutan[df_hutan["Kabupaten/Kota"] == pilihan_wilayah]["Total Kawasan Hutan (ha)"].values[0]
        
    st.write(f"Luas Kawasan Hutan Terpilih: {luas_analisis:,.2f} Hektar")
    
    col1, col2 = st.columns(2)
    with col1:
        nilai_langsung = st.number_input("Nilai Guna Langsung (Manfaat Hasil Kayu) - Rp/Tahun", value=int(luas_analisis * 5000))
        nilai_regulasi = st.number_input("Nilai Pengaturan (Jasa Karbon & Oksigen) - Rp/Tahun", value=int(luas_analisis * 10000))
    with col2:
        nilai_pilihan = st.number_input("Nilai Pilihan (Keanekaragaman Hayati) - Rp/Tahun", value=int(luas_analisis * 1500))
        nilai_eksistensi = st.number_input("Nilai Eksistensi (Kelestarian Ekosistem) - Rp/Tahun", value=int(luas_analisis * 1500))
        
    total_tev = nilai_langsung + nilai_regulasi + nilai_pilihan + nilai_eksistensi
    st.metric(label=f"NILAI EKONOMI TOTAL (TEV) - {pilihan_wilayah.upper()}", value=f"Rp {total_tev:,.2f}")
    
    st.subheader("Proporsi Kontribusi Struktur Nilai Ekonomi terhadap Ekosistem Hutan")
    df_pie_tev = pd.DataFrame({
        "Komponen Nilai": ["Guna Langsung", "Pengaturan/Regulasi", "Pilihan Masa Depan", "Eksistensi"],
        "Nilai Ekonomi (Rp)": [nilai_langsung, nilai_regulasi, nilai_pilihan, nilai_eksistensi]
    })
    
    fig_pie_tev = px.pie(
        df_pie_tev, 
        values="Nilai Ekonomi (Rp)", 
        names="Komponen Nilai", 
        title=f"Persentase Kontribusi Struktur TEV {pilihan_wilayah}"
    )
    st.plotly_chart(fig_pie_tev, use_container_width=True)

# =====================
# ANALISIS TRADE-OFF
# =====================

elif menu == "Analisis Trade-Off":
    st.subheader("Simulasi Substitusi Lahan")
    
    tradeoff = pd.DataFrame({
        "Skenario": ["Hutan Lestari", "Konversi Sawit", "Eksploitasi Kayu"],
        "Nilai Kelayakan (%)": [95, 65, 40]
    })

    fig = px.bar(tradeoff, x="Nilai Kelayakan (%)", y="Skenario", orientation="h", title="Perbandingan Nilai Kelayakan Antar Skenario")
    st.plotly_chart(fig, use_container_width=True)

# =====================
# PES
# =====================

elif menu == "PES":
    st.subheader("Simulasi Imbal Jasa Lingkungan")
    
    karbon_input = st.number_input("Cadangan Karbon (Ton)", value=172000000)
    harga_input = st.number_input("Harga Karbon (Rp/Ton)", value=150000)
    
    hasil = karbon_input * harga_input
    st.metric("Potensi Pendapatan PES", f"Rp {hasil:,.0f}")
