import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# =====================
# KONFIGURASI HALAMAN
# =====================

st.set_page_config(
    page_title="ECO-FOREST VALUATION HUTAN KALIMANTAN SELATAN",
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
# LOGO, JUDUL UTAMA & ATRIBUSI AKADEMIK
# =====================

try:
    logo = Image.open("logo.png")
    has_logo = True
except:
    has_logo = False

col_header1, col_header2 = st.columns([1, 5])

with col_header1:
    if has_logo:
        st.image(logo, width=110)
    else:
        st.warning("Logo tidak ditemukan")

with col_header2:
    st.title("ECO-FOREST VALUATION HUTAN KALIMANTAN SELATAN")
    st.write("Project Based Learning Ekonomi Sumber Daya Alam dan Lingkungan")
    
    st.markdown("<div><span style='color: #374151; font-weight: bold;'>Dosen Pengampu:</span> <span style='color: #DC2626; font-weight: bold;'>Yuhka Sundaya</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 15px; margin-bottom: 5px;'><span style='color: #1E3A8A; font-weight: bold; font-size: 15px;'>ANGGOTA KELOMPOK 9:</span></div>", unsafe_allow_html=True)
    
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        with st.container(border=True):
            st.markdown("<span style='color: #047857; font-weight: bold;'>Ina Rani Amelia</span><br><span style='color: #6B7280; font-size: 13px;'>NPM: 10090224002</span>", unsafe_allow_html=True)
    with col_k2:
        with st.container(border=True):
            st.markdown("<span style='color: #B45309; font-weight: bold;'>Nayla Dwi Safitri</span><br><span style='color: #6B7280; font-size: 13px;'>NPM: 10090224007</span>", unsafe_allow_html=True)
    with col_k3:
        with st.container(border=True):
            st.markdown("<span style='color: #4338CA; font-weight: bold;'>Celi Maulidi Aprilia</span><br><span style='color: #6B7280; font-size: 13px;'>NPM: 10090224027</span>", unsafe_allow_html=True)

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
    col3.metric("Cadangan Karbon (2024)", "113 Juta Ton")
    col4.metric("Total Pengunjung Wisata", "425 Ribu Orang/Tahun")

    st.write("Dashboard ini menyajikan data spasial dan valuasi ekonomi kehutanan Kalimantan Selatan.")
    st.dataframe(df_hutan.drop(columns=["Total Kawasan Hutan (ha)"]), use_container_width=True)
    
    df_urut = df_hutan.sort_values(by="Total Kawasan Hutan (ha)", ascending=False)
    kab_terluas = df_urut.iloc[0]["Kabupaten/Kota"]
    luas_terluas = df_urut.iloc[0]["Total Kawasan Hutan (ha)"]
    kab_terkecil = df_urut.iloc[-2]["Kabupaten/Kota"]
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_beranda = "Menu Beranda menyajikan gambaran umum mengenai profil fisik kawasan kehutanan di Kalimantan Selatan berdasarkan data Badan Pusat Statistik. Data mencakup agregasi total luas hutan dan sebaran spasial pada level kabupaten atau kota."
    
    analisis_beranda = f"""
    <div style="background-color: #F0FDF4; padding: 20px; border-left: 6px solid #16A34A; border-radius: 4px;">
        <h4 style="color: #166534; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Distribusi spasial kawasan hutan di Kalimantan Selatan menunjukkan ketimpangan geografis yang sangat tinggi. Kabupaten 
            <span style="color: #15803D; font-weight: bold;">{kab_terluas}</span> menguasai pangsa luas kawasan hutan terbesar sebesar 
            <span style="color: #111827; font-weight: bold;">{luas_terluas:,.2f} hektar</span>. Sebaliknya wilayah perkotaan seperti 
            <span style="color: #9A3412; font-weight: bold;">{kab_terkecil}</span> telah kehilangan hampir seluruh tutupan lahannya. Ketimpangan ini menuntut adanya diferensiasi kebijakan tata ruang. Wilayah dengan persentase hutan yang tinggi harus difokuskan pada optimalisasi insentif jasa ekosistem. Sebaliknya wilayah urban wajib didorong untuk menerapkan kebijakan kompensasi ruang terbuka hijau guna menyeimbangkan emisi karbon daerah.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_beranda}")
    st.markdown(analisis_beranda, unsafe_allow_html=True)

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
        title="Persentase Pembagian Kawasan Hutan Provinsi",
        color_discrete_sequence=px.colors.sequential.Darkmint
    )
    st.plotly_chart(fig_fungsi, use_container_width=True)
    st.dataframe(df_fungsi_total, use_container_width=True)
    
    total_produksi = total_hpt + total_hp + total_hpk
    rasio_produksi = (total_produksi / total_luas_provinsi) * 100
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_fungsi = "Menu Fungsi Hutan memetakan proporsi pemanfaatan lahan berdasarkan regulasi status hukum kawasan. Data diklasifikasikan menjadi fungsi konservasi, proteksi lindung, serta fungsi produksi kayu komersial."
    
    analisis_fungsi = f"""
    <div style="background-color: #FEF2F2; padding: 20px; border-left: 6px solid #DC2626; border-radius: 4px;">
        <h4 style="color: #991B1B; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Dominasi status hutan produksi yang mencapai <span style="color: #B91C1C; font-weight: bold;">{rasio_produksi:.2f}%</span> 
            dari total kawasan mencerminkan bahwa orientasi pemanfaatan hutan di Kalimantan Selatan masih padat karya eksploitatif. Tingginya porsi hutan produksi memicu ancaman eksternalitas negatif berupa degradasi habitat dan penurunan fungsi hidrologis daerah aliran sungai. Pemerintah daerah perlu memperketat kuota tebang tahunan. Pembatasan ini krusial untuk mencegah percepatan konversi lahan ke sektor non-kehutanan yang berisiko menurunkan kapasitas asimilasi lingkungan dalam jangka panjang.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_fungsi}")
    st.markdown(analisis_fungsi, unsafe_allow_html=True)

# =====================
# PROFIL SDA & JASA LINGKUNGAN
# =====================

elif menu == "Profil SDA & Jasa Lingkungan":
    st.header("Profil Sumber Daya Alam dan Jasa Lingkungan")
    st.write("Potensi kekayaan keanekaragaman hayati riil, kapasitas emisi serapan karbon, dan statistik industri ekowisata.")
    st.divider()
    
    st.subheader("1. Keanekaragaman Hayati (Biodiversitas)")
    col_bio1, col_bio2 = st.columns(2)
    
    with col_bio1:
        st.markdown("**Kekayaan Spesies Flora**")
        df_flora = pd.DataFrame({
            "Kelompok Famili": ["Dipterocarpaceae", "Myrtaceae", "Fabaceae", "Poaceae", "Orchidaceae"],
            "Jumlah Jenis": [420, 310, 280, 260, 190]
        })
        st.dataframe(df_flora, use_container_width=True)
        fig_flora = px.bar(df_flora, x="Jumlah Jenis", y="Kelompok Famili", orientation="h", title="Distribusi Famili Flora", color="Kelompok Famili", color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig_flora, use_container_width=True)
        
    with col_bio2:
        st.markdown("**Kekayaan Spesies Fauna**")
        df_fauna = pd.DataFrame({
            "Kelompok Taksonomi": ["Burung", "Ikan Air Tawar", "Mamalia", "Reptil", "Amfibi"],
            "Jumlah Spesies": [310, 120, 72, 68, 45]
        })
        st.dataframe(df_fauna, use_container_width=True)
        fig_fauna = px.bar(df_fauna, x="Jumlah Spesies", y="Kelompok Taksonomi", orientation="h", title="Distribusi Kelompok Fauna", color="Kelompok Taksonomi", color_discrete_sequence=px.colors.sequential.Oranges)
        st.plotly_chart(fig_fauna, use_container_width=True)
        
    st.divider()
    
    st.subheader("2. Kapasitas Volumetrik Keseimbangan Karbon Berkelanjutan")
    df_karbon = pd.DataFrame({
        "Tahun": ["2019", "2020", "2021", "2022", "2023", "2024"],
        "Emisi CO2 (Juta Ton)": [42, 45, 47, 49, 52, 54],
        "Serapan Karbon (Juta Ton)": [110, 108, 112, 109, 111, 113]
    })
    st.dataframe(df_karbon, use_container_width=True)
    
    fig_karbon_tren = px.line(df_karbon, x="Tahun", y=["Emisi CO2 (Juta Ton)", "Serapan Karbon (Juta Ton)"], markers=True, title="Tren Perbandingan Emisi Keseimbangan Karbon Tahunan", color_discrete_sequence=["#DC2626", "#16A34A"])
    st.plotly_chart(fig_karbon_tren, use_container_width=True)
    
    st.divider()
    
    st.subheader("3. Jasa Lingkungan Wisata Rekreasi Alam")
    df_wisata = pd.DataFrame({
        "Destinasi": ["Tahura Sultan Adam", "Pulau Kembang", "Loksado", "Air Terjun Haratai", "Meratus Trek"],
        "Kabupaten Administratif": ["Banjar", "Barito Kuala", "Hulu Sungai Selatan", "Hulu Sungai Selatan", "Hulu Sungai Tengah"],
        "Pengunjung (Ribu Orang/Tahun)": [120, 95, 85, 70, 60]
    })
    st.dataframe(df_wisata, use_container_width=True)
    
    fig_wisata = px.pie(df_wisata, names="Destinasi", values="Pengunjung (Ribu Orang/Tahun)", title="Pangsa Pasar Kunjungan Destinasi Ekowisata Hutan", color_discrete_sequence=px.colors.sequential.YlGnBu)
    st.plotly_chart(fig_wisata, use_container_width=True)
    
    total_spesies_flora = df_flora["Jumlah Jenis"].sum()
    total_spesies_fauna = df_fauna["Jumlah Spesies"].sum()
    net_serapan_2024 = df_karbon.iloc[-1]["Serapan Karbon (Juta Ton)"] - df_karbon.iloc[-1]["Emisi CO2 (Juta Ton)"]
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_sda = "Menu ini mengidentifikasi aset intangibel ekosistem hutan yang meliputi tingkat kerapatan keanekaragaman hayati, volume riil stok simpanan karbon, serta sebaran titik objek wisata alam."
    
    analisis_sda = f"""
    <div style="background-color: #F0FDF4; padding: 20px; border-left: 6px solid #16A34A; border-radius: 4px;">
        <h4 style="color: #166534; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Kekayaan biodiversitas sebanyak <span style="color: #15803D; font-weight: bold;">{total_spesies_flora} jenis flora</span> 
            dan <span style="color: #15803D; font-weight: bold;">{total_spesies_fauna} jenis fauna</span> membuktikan tingginya nilai modal alam intrinsik kawasan. Berdasarkan neraca asimilasi karbon tahun 2024, kapasitas penyerapan vegetasi hutan masih surplus dengan net asimilasi sebesar <span style="color: #111827; font-weight: bold;">{net_serapan_2024} juta ton CO2</span>. Fungsi penyerapan gas rumah kaca ini bertindak sebagai subsidi ekologis gratis bagi aktivitas industri daerah. Jasa lingkungan non-ekstraktif seperti objek wisata Tahura Sultan Adam yang mampu menarik <span style="color: #1D4ED8; font-weight: bold;">120 ribu pengunjung</span> merupakan substitusi mesin pertumbuhan ekonomi baru yang potensial. Investasi pada sektor pariwisata berbasis jasa alam ini wajib dikembangkan guna menggeser ketergantungan fiskal daerah dari sektor industri pertambangan yang merusak lingkungan.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_sda}")
    st.markdown(analisis_sda, unsafe_allow_html=True)

# =====================
# KALKULATOR TEV (TELAH DIPERBAIKI)
# =====================

elif menu == "Kalkulator TEV":
    st.header("Kalkulator Total Economic Value (TEV) & Simulasi Degradasi")
    st.write("Simulasi valuasi nilai ekonomi total ekosistem hutan serta analisis skenario kehilangan nilai akibat kerusakan lingkungan.")
    
    pilihan_wilayah = st.selectbox("Pilih Wilayah Analisis Simulasi:", ["Total Provinsi"] + list(df_hutan["Kabupaten/Kota"]))
    
    if pilihan_wilayah == "Total Provinsi":
        luas_analisis = total_luas_provinsi
    else:
        row_kab = df_hutan[df_hutan["Kabupaten/Kota"] == pilihan_wilayah].iloc[0]
        luas_analisis = row_kab["Total Kawasan Hutan (ha)"]
        
    st.info(f"Luas Geografis Hutan Teranalisis: {luas_analisis:,.2f} Hektar")
    st.divider()
    
    # ----------------------------------------------------------------
    # POIN 1: NILAI MANFAAT DASAR (KONDISI IDEAL BASELINE)
    # ----------------------------------------------------------------
    st.subheader("Poin 1: Nilai Manfaat Dasar (Kondisi Ideal Baseline)")
    
    tarif_langsung = st.slider("Nilai Guna Langsung (Hasil Kayu Finansial) - Rp/Ha/Tahun", min_value=1000, max_value=50000, value=15000, step=500)
    tarif_tidak_langsung = st.slider("Nilai Guna Tidak Langsung (Karbon & Oksigen) - Rp/Ha/Tahun", min_value=1000, max_value=50000, value=20000, step=500)
    tarif_pilihan = st.slider("Nilai Pilihan (Keanekaragaman Hayati & Wisata) - Rp/Ha/Tahun", min_value=1000, max_value=50000, value=15000, step=500)
    tarif_eksistensi = st.slider("Nilai Eksistensi (Warisan Kelestarian Hutan) - Rp/Ha/Tahun", min_value=1000, max_value=50000, value=10000, step=500)
    
    nilai_langsung_ideal = int(luas_analisis * tarif_langsung)
    nilai_tidak_langsung_ideal = int(luas_analisis * tarif_tidak_langsung)
    nilai_pilihan_ideal = int(luas_analisis * tarif_pilihan)
    nilai_eksistensi_ideal = int(luas_analisis * tarif_eksistensi)
    total_tev_ideal = nilai_langsung_ideal + nilai_tidak_langsung_ideal + nilai_pilihan_ideal + nilai_eksistensi_ideal
    
    st.metric(label="TEV Kondisi Ideal Baseline", value=f"Rp {total_tev_ideal:,.2f}")
    
    # Grafik Radar Parameter Poin 1
    categories_p1 = ["Guna Langsung", "Guna Tidak Langsung", "Nilai Pilihan", "Nilai Eksistensi"]
    fig_radar_p1 = go.Figure()
    fig_radar_p1.add_trace(go.Scatterpolar(
        r=[nilai_langsung_ideal, nilai_tidak_langsung_ideal, nilai_pilihan_ideal, nilai_eksistensi_ideal],
        theta=categories_p1,
        fill="toself",
        name="Kondisi Ideal Baseline",
        fillcolor="rgba(22, 163, 74, 0.2)",
        line=dict(color="#16A34A", width=3)
    ))
    fig_radar_p1.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showline=True, gridcolor="#E5E7EB"),
            angularaxis=dict(gridcolor="#E5E7EB")
        ),
        showlegend=True,
        title=dict(text=f"Parameter Struktur TEV Ideal Baseline {pilihan_wilayah}", font=dict(size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar_p1, use_container_width=True)
    
    # Penjelasan Mendalam Poin 1
    analisis_p1 = f"""
    <div style="background-color: #F0FDF4; padding: 20px; border-left: 6px solid #16A34A; border-radius: 4px; margin-bottom: 20px;">
        <h4 style="color: #166534; margin-top: 0;">Penjelasan Parameter Manfaat Dasar (Kondisi Ideal):</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Nilai modal alam tertinggi pada kondisi ideal baseline didominasi oleh nilai guna tidak langsung sebesar Rp {nilai_tidak_langsung_ideal:,.2f}, disusul oleh nilai guna langsung sebesar Rp {nilai_langsung_ideal:,.2f}. Akumulasi dari seluruh parameter manfaat dasar ini menghasilkan total kapasitas ekonomi awal sebesar Rp {total_tev_ideal:,.2f}. Angka ini menunjukkan bahwa fungsi ekologis hutan yang tidak masuk dalam pasar komersial tradisional, seperti regulasi air dan penyerapan karbon, memiliki kontribusi ekonomi intrinsik yang jauh lebih besar daripada hasil kayu fisik belaka.
        </p>
    </div>
    """
    st.markdown(analisis_p1, unsafe_allow_html=True)
    st.divider()
    
    # ----------------------------------------------------------------
    # POIN 2: PARAMETER KERUSAKAN & DEGRADASI HUTAN (KONDISI NYATA)
    # ----------------------------------------------------------------
    st.subheader("Poin 2: Parameter Kerusakan & Degradasi Hutan (Kondisi Nyata)")
    
    tingkat_deforestasi = st.slider("Tingkat Deforestasi (Persentase Luas Hutan yang Hilang)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
    faktor_degradasi_fungsi = st.slider("Penurunan Kualitas Ekosistem (Degradasi Fungsi Non-Pasar)", min_value=0.0, max_value=100.0, value=25.0, step=0.5)
    
    luas_tersisa = luas_analisis * (1 - (tingkat_deforestasi / 100))
    pengali_kualitas = 1 - (faktor_degradasi_fungsi / 100)
    
    nilai_langsung_nyata = int(luas_tersisa * tarif_langsung)
    nilai_tidak_langsung_nyata = int(luas_tersisa * tarif_tidak_langsung * pengali_kualitas)
    nilai_pilihan_nyata = int(luas_tersisa * tarif_pilihan * pengali_kualitas)
    nilai_eksistensi_nyata = int(luas_tersisa * tarif_eksistensi * pengali_kualitas)
    total_tev_nyata = nilai_langsung_nyata + nilai_tidak_langsung_nyata + nilai_pilihan_nyata + nilai_eksistensi_nyata
    
    total_kerugian = total_tev_ideal - total_tev_nyata
    persen_kerugian = (total_kerugian / total_tev_ideal) * 100 if total_tev_ideal > 0 else 0
    
    st.metric(label="TEV Riil Pasca Degradasi", value=f"Rp {total_tev_nyata:,.2f}", delta=f"-Rp {total_kerugian:,.2f}", delta_color="inverse")
    
    # Grafik Radar Parameter Poin 2
    fig_radar_p2 = go.Figure()
    fig_radar_p2.add_trace(go.Scatterpolar(
        r=[nilai_langsung_nyata, nilai_tidak_langsung_nyata, nilai_pilihan_nyata, nilai_eksistensi_nyata],
        theta=categories_p1,
        fill="toself",
        name="Pasca Deforestasi & Degradasi",
        fillcolor="rgba(220, 38, 38, 0.2)",
        line=dict(color="#DC2626", width=3)
    ))
    fig_radar_p2.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showline=True, gridcolor="#E5E7EB"),
            angularaxis=dict(gridcolor="#E5E7EB")
        ),
        showlegend=True,
        title=dict(text=f"Parameter Struktur TEV Pasca Degradasi {pilihan_wilayah}", font=dict(size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar_p2, use_container_width=True)
    
    # Penjelasan Mendalam Poin 2
    analisis_p2 = f"""
    <div style="background-color: #FEF2F2; padding: 20px; border-left: 6px solid #DC2626; border-radius: 4px; margin-bottom: 20px;">
        <h4 style="color: #991B1B; margin-top: 0;">Penjelasan Parameter Dampak Kerusakan (Kondisi Nyata):</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Pemberlakuan asumsi deforestasi sebesar {tingkat_deforestasi}% dan degradasi fungsi ekosistem sebesar {faktor_degradasi_fungsi}% mengontraksi seluruh parameter valuasi secara radikal. Nilai guna tidak langsung menyusut drastis menjadi Rp {nilai_tidak_langsung_nyata:,.2f}, dan nilai guna langsung berkurang menjadi Rp {nilai_langsung_nyata:,.2f}. Penurunan tajam pada grafik radar parameter ini merefleksikan kehancuran fisik tutupan lahan dan hilangnya kualitas asimilasi lingkungan yang riil di lapangan.
        </p>
    </div>
    """
    st.markdown(analisis_p2, unsafe_allow_html=True)
    st.divider()
    
    # ----------------------------------------------------------------
    # KESIMPULAN SECARA KESELURUHAN (TOTAL ECONOMIC VALUE)
    # ----------------------------------------------------------------
    st.subheader("Kesimpulan Akhir Analisis TEV")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric(label="TEV Kondisi Ideal Baseline", value=f"Rp {total_tev_ideal:,.2f}")
    col_m2.metric(label="TEV Riil Pasca Degradasi", value=f"Rp {total_tev_nyata:,.2f}")
    col_m3.metric(label="Total Kerugian Ekonomi", value=f"Rp {total_kerugian:,.2f}", delta=f"{persen_kerugian:.2f}% Penurunan", delta_color="inverse")
    
    deskripsi_tev = "Model simulasi kalkulator TEV mengintegrasikan penyusutan kuantitas luas hutan spasial dan penurunan kualitas fungsi ekologis secara simultan untuk mendeteksi total biaya kerusakan modal alam."
    
    analisis_kesimpulan = f"""
    <div style="background-color: #FFFBEB; padding: 20px; border-left: 6px solid #D97706; border-radius: 4px;">
        <h4 style="color: #92400E; margin-top: 0;">Kesimpulan Makro Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Kerusakan lingkungan pada ekosistem hutan {pilihan_wilayah} mengakibatkan konsekuensi finansial negatif yang masif bagi perekonomian daerah. Interaksi antara kehilangan luas lahan dan penurunan kualitas fungsi menurunkan nilai manfaat total dari Rp {total_tev_ideal:,.2f} menjadi hanya Rp {total_tev_nyata:,.2f}. Degradasi ini membebankan biaya kerugian eksternalitas atau marginal cost sosial sebesar Rp {total_kerugian:,.2f}, yang setara dengan kehilangan {persen_kerugian:.2f}% dari total aset modal alam. Fakta empiris ini menegaskan bahwa pembiaran terhadap laju deforestasi akan memicu biaya pemulihan ekologis jangka panjang yang jauh melampaui keuntungan ekonomi jangka pendek dari aktivitas eksploitasi hutan.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_tev}")
    st.markdown(analisis_kesimpulan, unsafe_allow_html=True)

# =====================
# ANALISIS TRADE-OFF
# =====================

elif menu == "Analisis Trade-Off":
    st.header("Analisis Trade-Off Substitusi Lahan dan Kebijakan Makro")
    st.write("Analisis tren akumulasi kerusakan akibat deforestasi hutan serta dampaknya terhadap peningkatan risiko bencana hidrometeorologi.")
    st.divider()
    
    col_to1, col_to2 = st.columns(2)
    
    with col_to1:
        st.subheader("Tren Akumulasi Kehilangan Hutan (Deforestasi)")
        df_defor = pd.DataFrame({
            "Tahun": ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"],
            "Kehilangan Hutan (ha)": [18500, 21000, 19500, 18000, 17500, 16000, 15000, 14500, 14000, 13800]
        })
        st.dataframe(df_defor, use_container_width=True)
        fig_defor = px.bar(df_defor, x="Tahun", y="Kehilangan Hutan (ha)", title="Luas Deforestasi Hutan Tahunan (Hektar)", color_discrete_sequence=["#EF4444"])
        st.plotly_chart(fig_defor, use_container_width=True)
        
    with col_to2:
        st.subheader("Korelasi Risiko Indikator Lingkungan")
        df_risiko = pd.DataFrame({
            "Tahun": ["2019", "2020", "2021", "2022", "2023", "2024"],
            "Hotspot Kebakaran": [1500, 900, 1100, 1400, 1600, 1000],
            "Kejadian Banjir": [55, 80, 72, 68, 75, 70]
        })
        st.dataframe(df_risiko, use_container_width=True)
        fig_risiko = px.scatter(df_risiko, x="Hotspot Kebakaran", y="Kejadian Banjir", text="Tahun", size="Kejadian Banjir", title="Matriks Korelasi Kebakaran Hutan dan Intensitas Banjir", color_discrete_sequence=["#D97706"])
        st.plotly_chart(fig_risiko, use_container_width=True)
        
    st.subheader("Simulasi Penentuan Bobot Prioritas Kebijakan Jangka Panjang")
    bobot_konservasi = st.slider("Fokus Terhadap Kompensasi Ekologis Jangka Panjang (%)", min_value=10, max_value=100, value=95, step=5)
    
    kelayakan_sawit = int(bobot_konservasi * 0.68)
    kelayakan_kayu = int(bobot_konservasi * 0.42)
    
    tradeoff = pd.DataFrame({
        "Skenario": ["Hutan Lestari", "Konversi Sawit", "Eksploitasi Kayu"],
        "Nilai Kelayakan (%)": [bobot_konservasi, kelayakan_sawit, kelayakan_kayu]
    })

    fig_bar_to = px.bar(tradeoff, x="Nilai Kelayakan (%)", y="Skenario", orientation="h", title="Perbandingan Nilai Kelayakan Antar Skenario Kebijakan", color="Skenario", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_bar_to, use_container_width=True)
    
    total_deforestasi = df_defor["Kehilangan Hutan (ha)"].sum()
    total_banjir = df_risiko["Kejadian Banjir"].sum()
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_tradeoff = "Menu Analisis Trade-Off mensimulasikan dampak pilihan kebijakan ekonomi terhadap keberlanjutan lingkungan. Modul ini membandingkan indeks kelayakan jangka panjang antara skenario konservasi penuh, konversi monokultur kelapa sawit, dan pembalakan kayu."
    
    analisis_tradeoff = f"""
    <div style="background-color: #FFFBEB; padding: 20px; border-left: 6px solid #D97706; border-radius: 4px;">
        <h4 style="color: #92400E; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Akumulasi kerusakan lahan akibat pembukaan hutan sepanjang dekade terakhir sangat masif dengan total kehilangan mencapai <span style="color: #B91C1C; font-weight: bold;">{total_deforestasi:,.0f} hektar</span> tutupan rimba. Dampak degradasi fisik ini berkorelasi langsung terhadap tingginya frekuensi bencana eksternalitas negatif dengan catatan total <span style="color: #B91C1C; font-weight: bold;">{total_banjir} kali kejadian banjir</span> merusak pemukiman warga. Saat target kelayakan jangka panjang dipatok pada angka <span style="color: #15803D; font-weight: bold;">{bobot_konservasi}%</span>, skenario konversi kelapa sawit hanya mampu mencapai indeks kelayakan <span style="color: #B45309; font-weight: bold;">{kelayakan_sawit}%</span> and pembalakan kayu turun drastis ke angka <span style="color: #B91C1C; font-weight: bold;">{kelayakan_kayu}%</span>. Angka ini secara ilmiah menunjukkan bahwa pilihan pembangunan ekstraktif tidak lagi layak dipertahankan karena memicu marginal cost sosial yang jauh lebih besar daripada revenue finansial privat yang dihasilkan.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_tradeoff}")
    st.markdown(analisis_tradeoff, unsafe_allow_html=True)

# =====================
# PES 
# =====================

elif menu == "PES":
    st.header("Simulasi Imbal Jasa Lingkungan (Payment for Ecosystem Services)")
    st.write("Analisis potensi penerimaan daerah melalui mekanisme pasar karbon internasional dan perbandingan elastisitas nilai antar jasa ekosistem.")
    st.divider()
    
    col_pes_in1, col_pes_in2 = st.columns(2)
    with col_pes_in1:
        karbon_input = st.slider(
            "Volume Cadangan Karbon Terfiksasi (Ton CO2)", 
            min_value=10000000, 
            max_value=200000000, 
            value=113000000, 
            step=1000000
        )
    with col_pes_in2:
        harga_input = st.slider(
            "Harga Karbon Acuan Regulasi Pasar (Rp/Ton CO2)", 
            min_value=50000, 
            max_value=500000, 
            value=150000, 
            step=5000
        )
        
    hasil = karbon_input * harga_input
    st.metric("Total Potensi Pendapatan Penerimaan Jasa Ekosistem (PES)", f"Rp {hasil:,.0f}")
    st.divider()
    
    st.subheader("1. Grafik Simulasi Sensitivitas Pendapatan PES Karbon")
    st.write("Grafik di bawah memproyeksikan perubahan total pendapatan daerah berdasarkan fluktuasi harga karbon di pasar internasional pada volume cadangan tetap.")
    
    rentang_harga = np.linspace(50000, 300000, 10)
    proyeksi_pendapatan = karbon_input * rentang_harga
    
    df_simulasi_pes = pd.DataFrame({
        "Harga Karbon Pasar (Rp/Ton)": rentang_harga,
        "Proyeksi Penerimaan Daerah (Rp)": proyeksi_pendapatan
    })
    
    fig_pes_line = px.line(
        df_simulasi_pes,
        x="Harga Karbon Pasar (Rp/Ton)",
        y="Proyeksi Penerimaan Daerah (Rp)",
        markers=True,
        title="Kurva Elastisitas Penerimaan Finansial PES Terhadap Harga Karbon Global",
        color_discrete_sequence=["#7C3AED"]
    )
    st.plotly_chart(fig_pes_line, use_container_width=True)
    st.divider()
    
    st.subheader("2. Matriks Perbandingan Potensi Antar Jasa Ekosistem Hutan")
    st.write("Perbandingan nilai moneter teoritis tahunan antar jenis pelayanan fungsi alam (Ecosystem Services) di Kalimantan Selatan.")
    
    nilai_regulasi_air = total_luas_provinsi * 25000
    nilai_wisata_alam = total_luas_provinsi * 12000
    nilai_opsi_farmasi = total_luas_provinsi * 8000
    
    df_komparasi_jasa = pd.DataFrame({
        "Klasifikasi Jasa Ekosistem": ["Penyerapan Karbon (PES)", "Regulasi Siklus Hidrologi", "Ekowisata & Rekreasi", "Opsi Keanekaragaman Farmasi"],
        "Estimasi Potensi Nilai (Rp/Tahun)": [hasil, nilai_regulasi_air, nilai_wisata_alam, nilai_opsi_farmasi],
        "Kategori Fungsi": ["Regulasi", "Regulasi", "Kultural", "Pilihan"]
    })
    
    df_komparasi_jasa = df_komparasi_jasa.sort_values(by="Estimasi Potensi Nilai (Rp/Tahun)", ascending=False)
    
    col_jasa1, col_jasa2 = st.columns([3, 2])
    with col_jasa1:
        fig_bar_jasa = go.Figure(go.Funnel(
            y=df_komparasi_jasa["Klasifikasi Jasa Ekosistem"],
            x=df_komparasi_jasa["Estimasi Potensi Nilai (Rp/Tahun)"],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=["#4C1D95", "#6D28D9", "#8B5CF6", "#A78BFA"],
                line=dict(width=1, color="#E5E7EB")
            ),
            connector=dict(line=dict(color="#C084FC", width=2))
        ))
        
        fig_bar_jasa.update_layout(
            title=dict(
                text="Struktur Hirarki Kontribusi Skala Ekonomi Potensi Jasa Ekosistem",
                font=dict(size=16)
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig_bar_jasa, use_container_width=True)
        
    with col_jasa2:
        st.write("Tabel Rincian Kontribusi Nilai Jasa Ekosistem")
        st.table(df_komparasi_jasa)
        
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_pes = "Menu PES (Payment for Ecosystem Services) atau Imbal Jasa Lingkungan menerapkan model kurva linear sensitivitas pasar untuk memetakan risiko harga instrumen karbon global. Penambahan matriks komparasi jasa ekosistem menyajikan perbandingan empiris kontribusi nilai ekonomi non-pasar secara sektoral."
    
    analisis_pes = f"""
    <div style="background-color: #FAF5FF; padding: 20px; border-left: 6px solid #7C3AED; border-radius: 4px;">
        <h4 style="color: #5B21B6; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Analisis kurva sensitivitas menunjukkan potensi penerimaan keuangan daerah yang sangat masif sebesar <span style="color: #1D4ED8; font-weight: bold;">Rp {hasil:,.0f}</span> dari hasil penjualan kredit karbon terfiksasi pada asumsi harga patokan nilai sebesar <span style="color: #B45309; font-weight: bold;">Rp {harga_input:,.0f}</span> per ton. Melalui visualisasi grafik komparasi jasa ekosistem, nilai ekonomi dari fungsi regulasi iklim terbukti mendominasi struktur modal alam non-pasar jauh melampaui potensi kultural ekowisata dan opsi farmasi. Realitas empiris ini membuktikan bahwa mempertahankan tutupan hutan sebagai penyerap karbon memberikan return sosial ekonomi yang jauh lebih stabil dibanding mengonversinya menjadi lahan industri ekstraktif. Dana kompensasi non-ekstraktif dari skema pasar internasional ini wajib dialokasikan secara berkeadilan untuk mendanai program insentif pelestarian hutan oleh masyarakat lokal guna menjamin keberlanjutan pasokan jasa lingkungan dalam jangka panjang.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_pes}")
    st.markdown(analisis_pes, unsafe_allow_html=True)
