import streamlit as st
import pandas as pd
import base64
import os
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(
    page_title="Eco-Forest Valuation Hutan Kalimantan Selatan", 
    layout="wide",
    initial_sidebar_state="expanded"
)

menu = st.sidebar.radio(
    "PILIH MODUL APLIKASI",
    [
        "Halaman Utama & Identitas",
        "Profile Hutan Kalimantan Selatan",
        "Modul Spasial: Peta KPH & Wilayah",
        "Modul 1: Kalkulator TEV", 
        "Modul 2: Trade-off Analisis", 
        "Modul 3: Kebijakan PES", 
        "Modul 4: Kasus Interaktif"
    ]
)

@st.cache_data
def load_base_data():
    data = {
        "Variabel": [
            "Luas Hutan Lindung (ha)", 
            "Luas Suaka Alam & Pelestarian Alam (ha)",
            "Luas Hutan Produksi Terbatas (ha)", 
            "Luas Hutan Produksi Tetap (ha)",
            "Luas Hutan Produksi Dapat Dikonversi (ha)", 
            "Produksi Kayu Bulat (m³)",
            "Produksi Kayu Gergajian (m³)", 
            "Produksi Kayu Lapis (m³)",
            "Produksi Veneer (m³)", 
            "Nilai Kayu (Rp/tahun)",
            "Nilai Karbon (Rp/tahun)", 
            "Nilai Oksigen (Rp/tahun)",
            "Total Nilai Ekonomi Langsung (Rp/tahun)"
        ],
        "Nilai": [
            507243.32, 216892.84, 123941.12, 685263.25, 119280.20,
            477250.17, 16082.54, 331057.94, 22991.57, 6991011291,
            379053921, 2117993021, 9488058736
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_kabupaten_data_fixed():
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
        "Hutan Produksi Konversi (ha)": [8788.74, 26960.68, 2037.31, 876.66, 6738.37, 18587.09, 0.00, 25861.33, 3697.69, 25732.33, 0.00, 0.00, 0.00],
        "Latitude": [-3.8168, -3.2444, -3.3150, -3.1667, -2.9333, -2.6833, -2.6167, -2.4167, -1.8333, -3.4500, -2.3333, -3.3167, -3.4167],
        "Longitude": [114.8667, 116.2167, 115.0000, 114.6667, 115.1500, 115.2500, 115.4167, 115.1667, 115.5000, 115.7000, 115.5000, 114.5917, 114.8333]
    }
    df = pd.DataFrame(data_kab)
    df["Total Kawasan Hutan (ha)"] = df.iloc[:, 1:6].sum(axis=1)
    return df

df_asli = load_base_data()
df_kabupaten = load_kabupaten_data_fixed()

if menu == "Halaman Utama & Identitas":
    st.title("ECO-FOREST VALUATION HUTAN KALIMANTAN SELATAN")
    st.subheader("Aplikasi Pembelajaran Ekonomi Sumber Daya Hutan Berbasis Streamlit")
    st.write("Fakultas Ekonomi dan Bisnis, Universitas Islam Bandung")
    st.write("---")
    st.markdown("### IDENTITAS MAHASISWA PENYUSUN")
    col1, col2, col3 = st.columns(3)
    col1.info("#### ANGGOTA 1\n**Ina Rani Amelia**\nNPM: 10090224002")
    col2.success("#### ANGGOTA 2\n**Nayla Dwi Safitri**\nNPM: 10090224013")
    col3.warning("#### ANGGOTA 3\n**Celi Maulidi Aprilia**\nNPM: 10090224027")

elif menu == "Profile Hutan Kalimantan Selatan":
    st.header("Profile Hutan Provinsi Kalimantan Selatan")
    st.subheader("1. Tata Guna Lahan dan Fungsi Ekologis Hutan Provinsi")
    
    df_melted = df_kabupaten.melt(id_vars=["Kabupaten/Kota"], value_vars=["Hutan Lindung (ha)", "Suaka Alam & Pelestarian (ha)", "Hutan Produksi Terbatas (ha)", "Hutan Produksi Tetap (ha)", "Hutan Produksi Konversi (ha)"], var_name="Fungsi Hutan", value_name="Luas (ha)")
    
    fig_pie = px.pie(df_melted, values="Luas (ha)", names="Fungsi Hutan", title="Proporsi Fungsi Kawasan Hutan Kalimantan Selatan")
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("2. Sebaran Kawasan Hutan Menurut Kabupaten/Kota")
    st.dataframe(df_kabupaten.drop(columns=["Latitude", "Longitude"]), use_container_width=True)

elif menu == "Modul Spasial: Peta KPH & Wilayah":
    st.header("Dasbor Spasial Pemantauan Kawasan Wilayah")
    st.write("Visualisasi lokasi koordinat pusat administratif kawasan hutan kabupaten dan kota di Kalimantan Selatan untuk memantau sebaran spasial.")
    
    m = folium.Map(location=[-3.0, 115.5], zoom_start=8)
    
    for idx, row in df_kabupaten.iterrows():
        if row["Total Kawasan Hutan (ha)"] > 0:
            popup_text = f"<b>{row['Kabupaten/Kota']}</b><br>Total Hutan: {row['Total Kawasan Hutan (ha)']:,.2f} ha<br>HL: {row['Hutan Lindung (ha)']:,.2f} ha"
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=popup_text,
                icon=folium.Icon(color="green", icon="tree")
            ).add_to(m)
            
            folium.Circle(
                location=[row["Latitude"], row["Longitude"]],
                radius=float(row["Total Kawasan Hutan (ha)"] * 0.1),
                color="darkgreen",
                fill=True,
                fill_color="green",
                fill_opacity=0.2
            ).add_to(m)
            
    st_folium(m, width=1100, height=500)

elif menu == "Modul 1: Kalkulator TEV":
    st.header("Modul 1: Kalkulator Total Economic Value (TEV)")
    pilihan_wilayah = st.selectbox("Pilih Cakupan Wilayah Perhitungan:", ["Total Provinsi Kalsel"] + list(df_kabupaten["Kabupaten/Kota"]))
    
    if pilihan_wilayah == "Total Provinsi Kalsel":
        luas_analisis = df_kabupaten["Total Kawasan Hutan (ha)"].sum()
        nilai_langsung_default = int(df_asli.iloc[9]['Nilai'])
        nilai_regulasi_default = int(df_asli.iloc[10]['Nilai'] + df_asli.iloc[11]['Nilai'])
    else:
        row_kab = df_kabupaten[df_kabupaten["Kabupaten/Kota"] == pilihan_wilayah].iloc[0]
        luas_analisis = row_kab["Total Kawasan Hutan (ha)"]
        proporsi_luas = luas_analisis / df_kabupaten["Total Kawasan Hutan (ha)"].sum()
        nilai_langsung_default = int(df_asli.iloc[9]['Nilai'] * proporsi_luas)
        nilai_regulasi_default = int((df_asli.iloc[10]['Nilai'] + df_asli.iloc[11]['Nilai']) * proporsi_luas)
        
    st.write(f"Luas Kawasan Hutan Terpilih: {luas_analisis:,.2f} Hektar")
    
    col1, col2 = st.columns(2)
    with col1:
        nilai_langsung = st.number_input("Nilai Guna Langsung (Manfaat Fisik Kayu) - Rp/Tahun", value=nilai_langsung_default)
        nilai_regulasi = st.number_input("Nilai Pengaturan (Jasa Karbon & Oksigen) - Rp/Tahun", value=nilai_regulasi_default)
    with col2:
        nilai_pilihan = st.number_input("Nilai Pilihan (Option Value Keanekaragaman Hayati) - Rp/Tahun", value=int(luas_analisis * 1500))
        nilai_eksistensi = st.number_input("Nilai Eksistensi (Existence Value Kelestarian) - Rp/Tahun", value=int(luas_analisis * 1500))
        
    total_tev = nilai_langsung + nilai_regulasi + nilai_pilihan + nilai_eksistensi
    st.metric(label=f"NILAI EKONOMI TOTAL (TEV) - {pilihan_wilayah.upper()}", value=f"Rp {total_tev:,.2f}")

elif menu == "Modul 2: Trade-off Analisis":
    st.header("Modul 2: Analisis Substitusi Lahan (Hutan vs Perkebunan)")
    pilihan_wilayah_trade = st.selectbox("Pilih Lokasi Simulasi Konversi:", list(df_kabupaten["Kabupaten/Kota"]))
    row_kab_trade = df_kabupaten[df_kabupaten["Kabupaten/Kota"] == pilihan_wilayah_trade].iloc[0]
    luas_maksimal = row_kab_trade["Total Kawasan Hutan (ha)"]
    
    st.write(f"Total Luas Kawasan Hutan di {pilihan_wilayah_trade}: {luas_maksimal:,.2f} Hektar")
    luas_konversi = st.slider("Asumsi Luas Kawasan Hutan yang Dikonversi (Hektar)", 0.0, float(luas_maksimal), 0.0)
    
    untung_sawit_per_ha = st.number_input("Rata-rata Keuntungan Sektor Perkebunan Komersial (Rp/Hektar/Tahun)", value=15000000)
    total_untung_konversi = luas_konversi * untung_sawit_per_ha
    total_rugi_hutan = luas_konversi * (9488058736 / df_kabupaten["Total Kawasan Hutan (ha)"].sum())
    manfaat_neto = total_untung_konversi - total_rugi_hutan
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Estimasi Manfaat Finansial Perkebunan", f"Rp {total_untung_konversi:,.2f}")
    col2.metric("Estimasi Kerugian Ekologis Hutan", f"Rp {total_rugi_hutan:,.2f}")
    col3.metric("Manfaat Bersih Kemakmuran (Net Benefit)", f"Rp {manfaat_neto:,.2f}")

elif menu == "Modul 3: Kebijakan PES":
    st.header("Modul 3: Simulasi Imbal Jasa Lingkungan (PES)")
    tarif_karbon = st.number_input("Harga Karbon Internasional Berlaku (Rp / Ton CO2)", value=150000)
    jumlah_karbon = st.number_input("Volume Penyerapan Karbon Tahunan (Ton CO2 / Tahun)", value=50000)
    total_dana_pes = tarif_karbon * jumlah_karbon
    st.metric("Total Potensi Penerimaan Insentif Pasar Karbon", f"Rp {total_dana_pes:,.2f}")

elif menu == "Modul 4: Kasus Interaktif":
    st.header("Modul 4: Studi Kasus Riil Ekonomi Lingkungan")
    pilihan_kasus = st.selectbox("Pilih Topik Kasus", ["Valuasi Serapan Karbon Pesisir", "Peran Jasa Penyerbukan Lebah"])
    if pilihan_kasus == "Valuasi Serapan Karbon Pesisir":
        panjang_pantai = st.number_input("Panjang Infrastruktur Alami Mangrove (Kilometer)", value=50)
        st.write(f"Nilai manfaat ekonomi tidak langsung penahanan abrasi: Rp {panjang_pantai * 100000000:,.2f} / tahun")
    else:
        luas_kebun = st.number_input("Luas Lahan Pertanian Sektor Hortikultura (Hektar)", value=5000)
        st.write(f"Nilai ekonomi dari aktivitas penyerbukan alami lebah: Rp {luas_kebun * 2000000:,.2f} / tahun")
