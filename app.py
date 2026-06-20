import streamlit as st
import pandas as pd
import base64
import os
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
    # PERBAIKAN: Seluruh nilai kosong berupa strip sudah diubah menjadi angka 0.0 agar terbaca oleh plotly express
    kab_data = {
        "Kabupaten/Kota": [
            "Tanah Laut", "Kota Baru", "Banjar", "Barito Kuala", "Tapin", 
            "Hulu Sungai Selatan", "Hulu Sungai Tengah", "Hulu Sungai Utara", 
            "Tabalong", "Tanah Bumbu", "Balangan", "Banjarmasin", "Banjarbaru"
        ],
        "Hutan Lindung": [13688.39, 149531.40, 44856.83, 144.90, 10150.96, 23484.74, 32174.60, 0.00, 26868.96, 5601.76, 11718.98, 0.00, 0.00],
        "Suaka Alam & Pelestarian": [27338.06, 83078.47, 97084.76, 3666.69, 0.00, 249.34, 0.00, 0.00, 0.00, 52402.43, 0.00, 0.00, 4122.23],
        "Produksi Terbatas": [5235.57, 881.23, 25103.68, 0.00, 841.51, 0.00, 0.00, 0.00, 0.00, 0.00, 4158.49, 0.00, 0.00],
        "Produksi Tetap": [70157.61, 241902.40, 82503.74, 0.00, 5840.76, 11250.48, 5971.05, 0.00, 31742.66, 127608.20, 19586.85, 0.00, 0.00],
        "Produksi Konversi": [8788.74, 26960.68, 2037.31, 876.66, 6738.37, 18587.09, 2191.01, 0.00, 15993.53, 2664.12, 11110.15, 0.00, 0.00]
    }
    return pd.DataFrame(kab_data)

df_asli = load_base_data()
df_kab = load_kabupaten_data()

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
    st.write("Gambaran biofisik, tata guna lahan, sebaran wilayah, dan kapasitas produksi komoditas kehutanan daerah.")
    
    st.write("---")
    
    st.subheader("1. Tata Guna Lahan dan Fungsi Ekologis Hutan")
    st.write("Alokasi spasial kawasan hutan terbagi menjadi lima fungsi pokok untuk menjaga keseimbangan neraca sumber daya alam.")
    
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
    col_f1.metric("Hutan Lindung", f"{df_asli.iloc[0]['Nilai']:,.2f} ha")
    col_f2.metric("Suaka Alam & Pelestarian", f"{df_asli.iloc[1]['Nilai']:,.2f} ha")
    col_f3.metric("Produksi Terbatas", f"{df_asli.iloc[2]['Nilai']:,.2f} ha")
    col_f4.metric("Produksi Tetap", f"{df_asli.iloc[3]['Nilai']:,.2f} ha")
    col_f5.metric("Produksi Konversi", f"{df_asli.iloc[4]['Nilai']:,.2f} ha")
    
    st.write("#### Grafik Lingkaran Proporsi Fungsi Kawasan Hutan Provinsi")
    df_pie_hutan = pd.DataFrame({
        "Fungsi Kawasan Hutan": ["Hutan Lindung", "Suaka Alam & Pelestarian", "Produksi Terbatas", "Produksi Tetap", "Produksi Konversi"],
        "Luas Lahan (ha)": [df_asli.iloc[0]['Nilai'], df_asli.iloc[1]['Nilai'], df_asli.iloc[2]['Nilai'], df_asli.iloc[3]['Nilai'], df_asli.iloc[4]['Nilai']]
    })
    fig_pie = px.pie(df_pie_hutan, values="Luas Lahan (ha)", names="Fungsi Kawasan Hutan", hole=0.3)
    fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.write("---")
    
    st.subheader("2. Sebaran Luas Hutan Menurut Kabupaten/Kota")
    st.write("Distribusi spasial luas kawasan hutan (dalam hektar) di 13 kabupaten/kota Provinsi Kalimantan Selatan.")
    
    # PERBAIKAN: Memastikan data luas bertipe float agar sumbu Y muncul otomatis
    df_melted = df_kab.melt(id_vars=["Kabupaten/Kota"], var_name="Fungsi Hutan", value_name="Luas (ha)")
    df_melted["Luas (ha)"] = df_melted["Luas (ha)"].astype(float)
    
    fig_bar = px.bar(
        df_melted, 
        x="Kabupaten/Kota", 
        y="Luas (ha)", 
        color="Fungsi Hutan", 
        title="Sebaran Komposisi Fungsi Hutan Per Kabupaten/Kota", 
        barmode="stack"
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.write("#### Tabel Data Spasial Kehutanan Daerah (ha)")
    st.dataframe(df_kab, use_container_width=True)
    
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
    st.write("Analisis kuantitatif komponen nilai guna dan nilai bukan guna berdasarkan data dasar.")
    
    st.subheader("Data Input Wilayah dan Hasil Hutan")
    st.dataframe(df_asli.iloc[0:9], use_container_width=True)
    
    st.subheader("Formulasi Valuasi Ekonomi")
    col1, col2 = st.columns(2)
    
    with col1:
        nilai_langsung = st.number_input("Nilai Guna Langsung (Manfaat Fisik Kayu) - Rp/Tahun", value=int(df_asli.iloc[9]['Nilai']))
        nilai_regulasi = st.number_input("Nilai Pengaturan (Jasa Karbon & Oksigen) - Rp/Tahun", value=int(df_asli.iloc[10]['Nilai'] + df_asli.iloc[11]['Nilai']))
    
    with col2:
        nilai_pilihan = st.number_input("Nilai Pilihan (Option Value Keanekaragaman Hayati) - Rp/Tahun", value=1500000000)
        nilai_eksistensi = st.number_input("Nilai Eksistensi (Existence Value Kelestarian) - Rp/Tahun", value=1500000000)
        
    total_tev = nilai_langsung + nilai_regulasi + nilai_pilihan + nilai_eksistensi
    
    st.write("### HASIL PERHITUNGAN TOTAL ECONOMIC VALUE")
    st.metric(label="NILAI EKONOMI TOTAL (TEV) HUTAN KALSEL", value=f"Rp {total_tev:,.2f}")
    
    persen_langsung = (nilai_langsung / total_tev) * 100
    persen_regulasi = (nilai_regulasi / total_tev) * 100
    persen_pilihan = (nilai_pilihan / total_tev) * 100
    persen_eksistensi = (nilai_eksistensi / total_tev) * 100
    
    st.subheader("Proporsi Kontribusi Nilai terhadap Ekosistem")
    chart_data = pd.DataFrame({
        "Kategori Nilai": ["Guna Langsung", "Pengaturan/Regulasi", "Pilihan Masa Depan", "Eksistensi"],
        "Persentase (%)": [persen_langsung, persen_regulasi, persen_pilihan, persen_eksistensi]
    })
    st.bar_chart(data=chart_data, x="Kategori Nilai", y="Persentase (%)")

elif menu == "Modul 2: Trade-off Analisis":
    st.header("Modul 2: Analisis Substitusi Lahan (Hutan vs Perkebunan)")
    st.write("Simulasi perbandingan kelayakan ekonomi konversi kawasan ekologis.")
    
    luas_total = df_asli.iloc[0:5]["Nilai"].sum()
    st.write(f"Total Luas Kawasan Hutan Terdata di Kalimantan Selatan: {luas_total:,.2f} Hektar")
    
    luas_konversi = st.slider("Asumsi Luas Kawasan Hutan yang Dikonversi (Hektar)", 0.0, luas_total, 10000.0)
    
    untung_sawit_per_ha = st.number_input("Rata-rata Keuntungan Sektor Perkebunan Komersial (Rp/Hektar/Tahun)", value=15000000)
    total_untung_konversi = luas_konversi * untung_sawit_per_ha
    
    nilai_hutan_per_ha = 9488058736 / luas_total
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
