import streamlit as st
import pandas as pd
import base64
import os

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
            308221.52, 267541.98, 31220.48, 394563.75, 38663.39,
            477250.17, 16082.54, 331057.94, 22991.57, 6991011291,
            379053921, 2117993021, 9488058736
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_kabupaten_data():
    data_kab = {
        "Kabupaten/Kota": [
            "Tanah Laut", "Kotabaru", "Banjar", "Barito Kuala", "Tapin", 
            "Hulu Sungai Selatan", "Hulu Sungai Tengah", "Hulu Sungai Utara", 
            "Tabalong", "Tanah Bumbu", "Balangan", "Banjarmasin", "Banjarbaru"
        ],
        "Hutan Lindung (ha)": [18314.00, 89422.00, 31405.00, 0.00, 5214.00, 24150.00, 29115.00, 0.00, 42150.00, 41215.00, 27236.52, 0.00, 0.00],
        "Suaka Alam & Pelestarian (ha)": [12150.00, 75410.00, 42115.00, 5412.00, 0.00, 14215.00, 0.00, 3120.00, 21450.00, 68214.98, 25450.00, 0.00, 0.00],
        "Hutan Produksi Terbatas (ha)": [4120.00, 8215.00, 0.00, 0.00, 2150.00, 0.00, 3120.00, 0.00, 5410.48, 6125.00, 2080.00, 0.00, 0.00],
        "Hutan Produksi Tetap (ha)": [25410.00, 115420.00, 38215.00, 0.00, 14250.00, 19150.00, 12140.00, 0.00, 68410.00, 78512.00, 22513.75, 0.00, 543.00],
        "Hutan Produksi Konversi (ha)": [3120.00, 12450.00, 2150.00, 0.00, 1150.00, 3215.00, 0.00, 0.00, 5120.00, 8215.39, 3243.00, 0.00, 0.00]
    }
    df = pd.DataFrame(data_kab)
    df["Total Kawasan Hutan (ha)"] = df.iloc[:, 1:6].sum(axis=1)
    return df

df_asli = load_base_data()
df_kabupaten = load_kabupaten_data()

def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

if menu == "Halaman Utama & Identitas":
    with st.container():
        col_logo, col_judul = st.columns([1, 4])
        
        with col_logo:
            img_base64 = get_image_base64("logo.png")
            if img_base64:
                st.markdown(f'<img src="data:image/png;base64,{img_base64}" width="150">', unsafe_allow_html=True)
            else:
                st.warning("File logo.png tidak ditemukan di repositori.")
            
        with col_judul:
            st.title("ECO-FOREST VALUATION HUTAN KALIMANTAN SELATAN")
            st.subheader("Aplikasi Pembelajaran Ekonomi Sumber Daya Hutan Berbasis Streamlit")
            st.write("Fakultas Ekonomi dan Bisnis, Universitas Islam Bandung")
            
    st.write("---")
    
    with st.container():
        st.markdown("### IDENTITAS MAHASISWA PENYUSUN")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("#### ANGGOTA 1\n**Ina Rani Amelia**\nNPM: 10090224002")
            
        with col2:
            st.success("#### ANGGOTA 2\n**Nayla Dwi Safitri**\nNPM: 10090224013")
            
        with col3:
            st.warning("#### ANGGOTA 3\n**Celi Maulidi Aprilia**\nNPM: 10090224027")
            
    st.write("---")
    st.info("Petunjuk Penggunaan: Silakan gunakan menu navigasi di sebelah kiri untuk mengakses setiap modul analisis ekonomi lingkungan.")

elif menu == "Profile Hutan Kalimantan Selatan":
    st.header("Profile Hutan Provinsi Kalimantan Selatan")
    st.write("Gambaran biofisik, tata guna lahan, dan kapasitas produksi komoditas kehutanan wilayah berdasarkan data makro.")
    
    st.write("---")
    
    st.subheader("1. Tata Guna Lahan dan Fungsi Ekologis Hutan Provinsi")
    st.write("Alokasi spasial kawasan hutan terbagi menjadi lima fungsi pokok untuk menjaga keseimbangan neraca sumber daya alam.")
    
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
    col_f1.metric("Hutan Lindung", f"{df_asli.iloc[0]['Nilai']:,.2f} ha")
    col_f2.metric("Suaka Alam & Pelestarian", f"{df_asli.iloc[1]['Nilai']:,.2f} ha")
    col_f3.metric("Produksi Terbatas", f"{df_asli.iloc[2]['Nilai']:,.2f} ha")
    col_f4.metric("Produksi Tetap", f"{df_asli.iloc[3]['Nilai']:,.2f} ha")
    col_f5.metric("Produksi Konversi", f"{df_asli.iloc[4]['Nilai']:,.2f} ha")
    
    st.write("#### Grafik Distribusi Luas Kawasan Hutan Provinsi (Hektar)")
    df_grafik_hutan = pd.DataFrame({
        "Fungsi Kawasan Hutan": [
            "Hutan Lindung", 
            "Suaka Alam & Pelestarian", 
            "Produksi Terbatas", 
            "Produksi Tetap", 
            "Produksi Konversi"
        ],
        "Luas Lahan (ha)": [
            df_asli.iloc[0]['Nilai'],
            df_asli.iloc[1]['Nilai'],
            df_asli.iloc[2]['Nilai'],
            df_asli.iloc[3]['Nilai'],
            df_asli.iloc[4]['Nilai']
        ]
    })
    st.bar_chart(data=df_grafik_hutan, x="Fungsi Kawasan Hutan", y="Luas Lahan (ha)")
    
    st.write("---")
    
    st.subheader("2. Sebaran Kawasan Hutan Menurut Kabupaten/Kota")
    st.write("Data rincian luas fungsi kawasan hutan pada 13 wilayah administratif di Kalimantan Selatan.")
    st.dataframe(df_kabupaten, use_container_width=True)
    
    st.write("#### Grafik Distribusi Luas Hutan Wilayah (Visualisasi Komparatif Area)")
    df_area = df_kabupaten.set_index("Kabupaten/Kota")[["Total Kawasan Hutan (ha)"]]
    st.area_chart(df_area)
    
    st.write("---")
    
    st.subheader("3. Kapasitas Produksi Hasil Hutan Kayu")
    st.write("Volume ekstraksi fisik komoditas kayu komersial yang menjadi roda penggerak sektor kehutanan daerah.")
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    col_p1.metric("Kayu Bulat", f"{df_asli.iloc[5]['Nilai']:,.2f} m³")
    col_p2.metric("Kayu Gergajian", f"{df_asli.iloc[6]['Nilai']:,.2f} m³")
    col_p3.metric("Kayu Lapis", f"{df_asli.iloc[7]['Nilai']:,.2f} m³")
    col_p4.metric("Veneer", f"{df_asli.iloc[8]['Nilai']:,.2f} m³")
    
    st.write("---")
    
    st.subheader("4. Neraca Potensi Nilai Guna Langsung Kasar")
    st.write("Akumulasi nilai ekonomi dari hasil pemanfaatan fisik kayu tahunan di Kalimantan Selatan.")
    st.metric(label="Total Estimasi Nilai Guna Langsung Kayu", value=f"Rp {df_asli.iloc[9]['Nilai']:,.2f} / tahun")

elif menu == "Modul 1: Kalkulator TEV":
    st.header("Modul 1: Kalkulator Total Economic Value (TEV)")
    st.write("Analisis kuantitatif komponen nilai guna dan nilai bukan guna berdasarkan data spasial kabupaten.")
    
    st.subheader("Pilih Wilayah Analisis Valuasi")
    pilihan_wilayah = st.selectbox("Pilih Cakupan Wilayah Perhitungan:", ["Total Provinsi Kalsel"] + list(df_kabupaten["Kabupaten/Kota"]))
    
    if pilihan_wilayah == "Total Provinsi Kalsel":
        luas_analisis = df_asli.iloc[0:5]["Nilai"].sum()
        nilai_langsung_default = int(df_asli.iloc[9]['Nilai'])
        nilai_regulasi_default = int(df_asli.iloc[10]['Nilai'] + df_asli.iloc[11]['Nilai'])
    else:
        row_kab = df_kabupaten[df_kabupaten["Kabupaten/Kota"] == pilihan_wilayah].iloc[0]
        luas_analisis = row_kab["Total Kawasan Hutan (ha)"]
        proporsi_luas = luas_analisis / df_asli.iloc[0:5]["Nilai"].sum()
        nilai_langsung_default = int(df_asli.iloc[9]['Nilai'] * proporsi_luas)
        nilai_regulasi_default = int((df_asli.iloc[10]['Nilai'] + df_asli.iloc[11]['Nilai']) * proporsi_luas)
        
    st.write(f"Luas Kawasan Hutan Terpilih: {luas_analisis:,.2f} Hektar")
    
    st.subheader("Formulasi Valuasi Ekonomi Interaktif")
    col1, col2 = st.columns(2)
    
    with col1:
        nilai_langsung = st.number_input("Nilai Guna Langsung (Manfaat Fisik Kayu) - Rp/Tahun", value=nilai_langsung_default)
        nilai_regulasi = st.number_input("Nilai Pengaturan (Jasa Karbon & Oksigen) - Rp/Tahun", value=nilai_regulasi_default)
    
    with col2:
        nilai_pilihan = st.number_input("Nilai Pilihan (Option Value Keanekaragaman Hayati) - Rp/Tahun", value=int(luas_analisis * 1500))
        nilai_eksistensi = st.number_input("Nilai Eksistensi (Existence Value Kelestarian) - Rp/Tahun", value=int(luas_analisis * 1500))
        
    total_tev = nilai_langsung + nilai_regulasi + nilai_pilihan + nilai_eksistensi
    
    st.write("### HASIL PERHITUNGAN TOTAL ECONOMIC VALUE")
    st.metric(label=f"NILAI EKONOMI TOTAL (TEV) - {pilihan_wilayah.upper()}", value=f"Rp {total_tev:,.2f}")
    
    if total_tev > 0:
        persen_langsung = (nilai_langsung / total_tev) * 100
        persen_regulasi = (nilai_regulasi / total_tev) * 100
        persen_pilihan = (nilai_pilihan / total_tev) * 100
        persen_eksistensi = (nilai_eksistensi / total_tev) * 100
    else:
        persen_langsung = persen_regulasi = persen_pilihan = persen_eksistensi = 0
    
    st.subheader("Proporsi Kontribusi Nilai terhadap Ekosistem (Tren Kontribusi Line Chart)")
    chart_data = pd.DataFrame({
        "Persentase (%)": [persen_langsung, persen_regulasi, persen_pilihan, persen_eksistensi]
    }, index=["Guna Langsung", "Pengaturan/Regulasi", "Pilihan Masa Depan", "Eksistensi"])
    st.line_chart(data=chart_data)

elif menu == "Modul 2: Trade-off Analisis":
    st.header("Modul 2: Analisis Substitusi Lahan (Hutan vs Perkebunan)")
    st.write("Simulasi perbandingan kelayakan ekonomi konversi kawasan ekologis berbasis data wilayah.")
    
    pilihan_wilayah_trade = st.selectbox("Pilih Lokasi Simulasi Konversi:", list(df_kabupaten["Kabupaten/Kota"]))
    row_kab_trade = df_kabupaten[df_kabupaten["Kabupaten/Kota"] == pilihan_wilayah_trade].iloc[0]
    luas_maksimal = row_kab_trade["Total Kawasan Hutan (ha)"]
    
    st.write(f"Total Luas Kawasan Hutan di {pilihan_wilayah_trade}: {luas_maksimal:,.2f} Hektar")
    
    luas_konversi = st.slider("Asumsi Luas Kawasan Hutan yang Dikonversi (Hektar)", 0.0, float(luas_maksimal), float(luas_maksimal * 0.1 if luas_maksimal * 0.1 > 0 else 0.0))
    
    untung_sawit_per_ha = st.number_input("Rata-rata Keuntungan Sektor Perkebunan Komersial (Rp/Hektar/Tahun)", value=15000000)
    total_untung_konversi = luas_konversi * untung_sawit_per_ha
    
    nilai_hutan_per_ha = 9488058736 / df_asli.iloc[0:5]["Nilai"].sum()
    total_rugi_hutan = luas_konversi * nilai_hutan_per_ha
    
    manfaat_neto = total_untung_konversi - total_rugi_hutan
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Estimasi Manfaat Finansial Perkebunan", f"Rp {total_untung_konversi:,.2f}")
    col2.metric("Estimasi Kerugian Ekologis Hutan", f"Rp {total_rugi_hutan:,.2f}")
    col3.metric("Manfaat Bersih Kemakmuran (Net Benefit)", f"Rp {manfaat_neto:,.2f}")
    
    if manfaat_neto < 0:
        st.error("Rekomendasi Kebijakan: Tolak Konversi Lahan. Kerugian fungsi ekosistem melampaui keuntungan finansial.")
    else:
        st.success("Rekomendasi Kebijakan: Konversi Secara Terbatas Dapat Dipertimbangkan dengan Pengawasan Ketat.")

elif menu == "Modul 3: Kebijakan PES":
    st.header("Modul 3: Simulasi Imbal Jasa Lingkungan (PES)")
    st.write("Analisis instrumen pasar untuk menciptakan insentif ekonomi bagi masyarakat sekitar hutan.")
    
    tarif_karbon = st.number_input("Harga Karbon Internasional Berlaku (Rp / Ton CO2)", value=150000)
    jumlah_karbon = st.number_input("Volume Penyerapan Karbon Tahunan (Ton CO2 / Tahun)", value=50000)
    
    total_dana_pes = tarif_karbon * jumlah_karbon
    st.metric("Total Potensi Penerimaan Insentif Pasar Karbon", f"Rp {total_dana_pes:,.2f}")
    
    biaya_patroli = st.number_input("Alokasi Biaya Perlindungan & Patroli Hutan (Rp / Tahun)", value=500000000)
    sisa_dana = total_dana_pes - biaya_patroli
    
    st.write(f"Dana mengendap untuk distribusi kesejahteraan komunitas lokal: Rp {sisa_dana:,.2f}")

elif menu == "Modul 4: Kasus Interaktif":
    st.header("Modul 4: Studi Kasus Riil Ekonomi Lingkungan")
    st.write("Eksplorasi interaktif mengenai keterkaitan ekosistem dan aktivitas ekonomi.")
    
    pilihan_kasus = st.selectbox("Pilih Topik Kasus", ["Valuasi Serapan Karbon Pesisir", "Peran Jasa Penyerbukan Lebah"])
    
    if pilihan_kasus == "Valuasi Serapan Karbon Pesisir":
        st.write("Analisis manfaat ekosistem mangrove dalam mereduksi dampak abrasi air laut.")
        panjang_pantai = st.number_input("Panjang Infrastruktur Alami Mangrove (Kilometer)", value=50)
        nilai_abrasi = panjang_pantai * 100000000
        st.write(f"Nilai manfaat ekonomi tidak langsung penahanan abrasi: Rp {nilai_abrasi:,.2f} / tahun")
    else:
        st.write("Analisis nilai ketergantungan komoditas hortikultura terhadap keberadaan fauna hutan.")
        luas_kebun = st.number_input("Luas Lahan Pertanian Sektor Hortikultura (Hektar)", value=5000)
        nilai_tambah_production = luas_kebun * 2000000
        st.write(f"Nilai ekonomi dari aktivitas penyerbukan alami lebah: Rp {nilai_tambah_production:,.2f} / tahun")
