import streamlit as st
import pandas as pd
import plotly.express as px
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
            st.markdown("<span style='color: #B45309; font-weight: bold;'>Nayla Dwi Safitri</span><br><span style='color: #6B7280; font-size: 13px;'>NPM: 10090224013</span>", unsafe_allow_html=True)
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
    total_proteksi = total_lindung + total_suaka
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
# KALKULATOR TEV (FITUR SIMULASI KERUSAKAN & DEGRADASI BARU)
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
    
    # Pembagian grid input: parameter tarif dasar dan parameter kerusakan
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("1. Nilai Manfaat Dasar (Rp / Hektar / Tahun)")
        tarif_langsung = st.slider("Nilai Guna Langsung (Hasil Kayu Finansial)", min_value=1000, max_value=50000, value=15000, step=500)
        tarif_tidak_langsung = st.slider("Nilai Guna Tidak Langsung (Karbon & Oksigen)", min_value=1000, max_value=50000, value=20000, step=500)
        tarif_pilihan = st.slider("Nilai Pilihan (Keanekaragaman Hayati & Wisata)", min_value=1000, max_value=50000, value=15000, step=500)
        tarif_eksistensi = st.slider("Nilai Eksistensi (Warisan Kelestarian Hutan)", min_value=1000, max_value=50000, value=10000, step=500)
        
    with col_input2:
        st.subheader("2. Parameter Kerusakan & Degradasi Hutan")
        tingkat_deforestasi = st.slider("Tingkat Deforestasi (Persentase Luas Hutan yang Hilang)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
        faktor_degradasi_fungsi = st.slider("Penurunan Kualitas Ekosistem (Degradasi Fungsi Non-Pasar)", min_value=0.0, max_value=100.0, value=25.0, step=0.5)
        
    # Perhitungan dampak kerusakan fisik
    luas_tersisa = luas_analisis * (1 - (tingkat_deforestasi / 100))
    
    # Kalkulasi TEV Kondisi Ideal Baseline
    nilai_langsung_ideal = int(luas_analisis * tarif_langsung)
    nilai_tidak_langsung_ideal = int(luas_analisis * tarif_tidak_langsung)
    nilai_pilihan_ideal = int(luas_analisis * tarif_pilihan)
    nilai_eksistensi_ideal = int(luas_analisis * tarif_eksistensi)
    total_tev_ideal = nilai_langsung_ideal + nilai_tidak_langsung_ideal + nilai_pilihan_ideal + nilai_eksistensi_ideal
    
    # Kalkulasi TEV Riil Pasca Kerusakan Lingkungan
    nilai_langsung_nyata = int(luas_tersisa * tarif_langsung)
    pengali_kualitas = 1 - (faktor_degradasi_fungsi / 100)
    nilai_tidak_langsung_nyata = int(luas_tersisa * tarif_tidak_langsung * pengali_kualitas)
    nilai_pilihan_nyata = int(luas_tersisa * tarif_pilihan * pengali_kualitas)
    nilai_eksistensi_nyata = int(luas_tersisa * tarif_eksistensi * pengali_kualitas)
    total_tev_nyata = nilai_langsung_nyata + nilai_tidak_langsung_nyata + nilai_pilihan_nyata + nilai_eksistensi_nyata
    
    # Perhitungan nilai ekonomi yang hilang (Marginal Cost Lingkungan)
    total_kerugian = total_tev_ideal - total_tev_nyata
    persen_kerugian = (total_kerugian / total_tev_ideal) * 100 if total_tev_ideal > 0 else 0
    
    st.divider()
    
    # Tampilan Dashboard Metrik Komparasi Kerusakan
    st.subheader("Hasil Estimasi Dampak Ekonomi")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric(label="TEV Kondisi Ideal Baseline", value=f"Rp {total_tev_ideal:,.2f}")
    col_m2.metric(label="TEV Riil Pasca Degradasi", value=f"Rp {total_tev_nyata:,.2f}", delta=f"-Rp {total_kerugian:,.2f}", delta_color="inverse")
    col_m3.metric(label="Total Kerugian Ekonomi (Marginal Cost)", value=f"Rp {total_kerugian:,.2f}", delta=f"{persen_kerugian:.2f}% Penurunan", delta_color="inverse")
    
    # Menyiapkan data untuk visualisasi grafik batang komparatif berkelompok
    df_visual_tev = pd.DataFrame({
        "Komponen Klasifikasi Nilai": ["Guna Langsung", "Guna Tidak Langsung", "Nilai Pilihan", "Nilai Eksistensi"] * 2,
        "Nilai Moneter (Rp)": [nilai_langsung_ideal, nilai_tidak_langsung_ideal, nilai_pilihan_ideal, nilai_eksistensi_ideal,
                               nilai_langsung_nyata, nilai_tidak_langsung_nyata, nilai_pilihan_nyata, nilai_eksistensi_nyata],
        "Skenario Kondisi Hutan": ["Kondisi Ideal Baseline"] * 4 + ["Pasca Deforestasi & Degradasi"] * 4
    })
    
    fig_perbandingan_tev = px.bar(
        df_visual_tev,
        x="Komponen Klasifikasi Nilai",
        y="Nilai Moneter (Rp)",
        color="Skenario Kondisi Hutan",
        barmode="group",
        title=f"Analisis Komparatif Kerusakan Struktur TEV Kawasan {pilihan_wilayah}",
        color_discrete_sequence=["#16A34A", "#DC2626"]
    )
    st.plotly_chart(fig_perbandingan_tev, use_container_width=True)
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_tev = "Menu Kalkulator TEV menerapkan model simulasi kerusakan dinamis untuk mendeteksi penyusutan aset modal alam. Integrasi variabel deforestasi spasial dan koefisien degradasi ekosistem menyajikan estimasi biaya kerusakan lingkungan yang riil."
    
    analisis_tev = f"""
    <div style="background-color: #FFFBEB; padding: 20px; border-left: 6px solid #D97706; border-radius: 4px;">
        <h4 style="color: #92400E; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Simulasi kerusakan pada ekosistem hutan {pilihan_wilayah} membuktikan bahwa kombinasi deforestasi lahan sebesar 
            <span style="color: #B91C1C; font-weight: bold;">{tingkat_deforestasi}%</span> dan degradasi kualitas fungsi ekologis sebesar 
            <span style="color: #B91C1C; font-weight: bold;">{faktor_degradasi_fungsi}%</span> memicu dampak finansial negatif yang sangat masif. Kerusakan tersebut mereduksi nilai ekonomi kawasan dari Rp {total_tev_ideal:,.2f} menjadi tersisa hanya 
            <span style="color: #15803D; font-weight: bold;">Rp {total_tev_nyata:,.2f}</span>. Hal ini menimbulkan kerugian ekonomi eksternalitas atau marginal cost sosial sebesar 
            <span style="color: #B91C1C; font-weight: bold;">Rp {total_kerugian:,.2f}</span>, yang setara dengan kehilangan 
            <span style="color: #B91C1C; font-weight: bold;">{persen_kerugian:.2f}%</span> dari total kapasitas utilitas modal alam. Penyusutan nilai terbesar terkonsentrasi pada fungsi non-pasar seperti nilai guna tidak langsung dan eksistensi. Fakta empiris ini menegaskan bahwa kegagalan mengendalikan laju kerusakan hutan akan membebankan biaya pemulihan ekologis yang jauh melampaui keuntungan ekonomi jangka pendek dari eksploitasi lahan.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_tev}")
    st.markdown(analisis_tev, unsafe_allow_html=True)

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
            Akumulasi kerusakan lahan akibat pembukaan hutan sepanjang dekade terakhir sangat masif dengan total kehilangan mencapai <span style="color: #B91C1C; font-weight: bold;">{total_deforestasi:,.0f} hektar</span> tutupan rimba. Dampak degradasi fisik ini berkorelasi langsung terhadap tingginya frekuensi bencana eksternalitas negatif dengan catatan total <span style="color: #B91C1C; font-weight: bold;">{total_banjir} kali kejadian banjir</span> merusak pemukiman warga. Saat target kelayakan jangka panjang dipatok pada angka <span style="color: #15803D; font-weight: bold;">{bobot_konservasi}%</span>, skenario konversi kelapa sawit hanya mampu mencapai indeks kelayakan <span style="color: #B45309; font-weight: bold;">{kelayakan_sawit}%</span> dan pembalakan kayu turun drastis ke angka <span style="color: #B91C1C; font-weight: bold;">{kelayakan_kayu}%</span>. Angka ini secara ilmiah menunjukkan bahwa pilihan pembangunan ekstraktif tidak lagi layak dipertahankan karena memicu marginal cost sosial yang jauh lebih besar daripada revenue finansial privat yang dihasilkan.
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
    st.subheader("Simulasi Imbal Jasa Lingkungan")
    
    karbon_input = st.number_input("Cadangan Karbon Terfiksasi (Ton)", value=113000000)
    harga_input = st.number_input("Harga Karbon Berdasarkan Regulasi Pasar (Rp/Ton)", value=150000)
    
    hasil = karbon_input * harga_input
    st.metric("Potensi Pendapatan Penerimaan Jasa Ekosistem (PES)", f"Rp {hasil:,.0f}")
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_pes = "Menu PES (Payment for Ecosystem Services) atau Imbal Jasa Lingkungan mensimulasikan instrumen pasar modern untuk konservasi. Sistem mengalkulasi potensi penerimaan dana segar yang diperoleh daerah melalui skema perdagangan karbon internasional."
    
    analisis_pes = f"""
    <div style="background-color: #FAF5FF; padding: 20px; border-left: 6px solid #7C3AED; border-radius: 4px;">
        <h4 style="color: #5B21B6; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Simulasi menunjukkan potensi penerimaan keuangan daerah yang sangat masif sebesar <span style="color: #1D4ED8; font-weight: bold;">Rp {hasil:,.0f}</span> 
            dari hasil optimalisasi insentif pasar internasional dengan asumsi harga patokan nilai sebesar <span style="color: #B45309; font-weight: bold;">Rp {harga_input:,.0f}</span> per ton karbon. Skema perdagangan karbon merubah paradigma pengelolaan lingkungan dari pusat beban pembiayaan pasif menjadi motor penggerak pendapatan asli daerah yang prospektif. Dana kompensasi non-ekstraktif ini wajib didistribusikan secara berkeadilan untuk mendanai program insentif pelestarian hutan rakyat oleh masyarakat lokal. Pendekatan insentif ekonomi ini menciptakan keselarasan jangka panjang antara target pertumbuhan ekonomi makro wilayah dan komitmen penurunan emisi gas rumah kaca global.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_pes}")
    st.markdown(analisis_pes, unsafe_allow_html=True)
