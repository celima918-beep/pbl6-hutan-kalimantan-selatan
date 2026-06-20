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
    col3.metric("Cadangan Karbon", "172 Juta Ton")
    col4.metric("Destinasi Wisata", "5 Lokasi Utama")

    st.write("Dashboard ini menyajikan data spasial dan valuasi ekonomi kehutanan Kalimantan Selatan.")
    st.dataframe(df_hutan.drop(columns=["Total Kawasan Hutan (ha)"]), use_container_width=True)
    
    df_urut = df_hutan.sort_values(by="Total Kawasan Hutan (ha)", ascending=False)
    kab_terluas = df_urut.iloc[0]["Kabupaten/Kota"]
    luas_terluas = df_urut.iloc[0]["Total Kawasan Hutan (ha)"]
    kab_terkecil = df_urut.iloc[-2]["Kabupaten/Kota"]
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_beranda = "Menu Beranda menyajikan gambaran umum mengenai profil fisik kawasan kehutanan di Kalimantan Selatan berdasarkan basis data Badan Pusat Statistik. Data mencakup agregasi total luas hutan dan sebaran spasial pada level kabupaten atau kota."
    
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
        fig_bio = px.bar(data_bio, x="Kategori", y="Jumlah Kerapatan Spesies", title="Perbandingan Kerapatan Spesies Kehutanan", color="Kategori", color_discrete_sequence=px.colors.qualitative.Set2)
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
        fig_karbon = px.pie(data_karbon, names="Kategori Parameter", values="Volume (Ton)", title="Proporsi Distribusi Aspek Karbon", color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_karbon, use_container_width=True)
        
    st.divider()
    st.subheader("3. Jasa Lingkungan Wisata Rekreasi Alam")
    data_wisata = pd.DataFrame({
        "Destinasi": ["Loksado", "Tahura Sultan Adam", "Pegunungan Meratus", "Air Terjun Haratai", "Pulau Kembang"],
        "Kawasan Administratif": ["Hulu Sungai Selatan", "Banjar/Banjarbaru", "Hulu Sungai Tengah", "Hulu Sungai Selatan", "Barito Kuala"]
    })
    st.dataframe(data_wisata, use_container_width=True)
    
    stok_karbon = data_karbon.iloc[0]["Volume (Ton)"]
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_sda = "Menu ini mengidentifikasi aset intangibel ekosistem hutan yang meliputi tingkat kerapatan keanekaragaman hayati, volume riil stok simpanan karbon, serta sebaran titik objek wisata alam."
    
    analisis_sda = f"""
    <div style="background-color: #F0FDF4; padding: 20px; border-left: 6px solid #16A34A; border-radius: 4px;">
        <h4 style="color: #166534; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Kekayaan biodiversitas dan volume cadangan karbon sebesar <span style="color: #15803D; font-weight: bold;">{stok_karbon:,.0f} ton</span> 
            membuktikan bahwa nilai ekologis hutan jauh melampaui nilai komoditas kayu domestik. Jasa lingkungan non-ekstraktif seperti objek wisata Tahura Sultan Adam dan Loksado merupakan penggerak ekonomi baru yang minim emisi. Pengembangan sektor ekowisata ini harus dikelola secara ketat menggunakan analisis batas ambang daya dukung lingkungan. Langkah tersebut diperlukan agar aktivitas rekreasi massal tidak merusak kelestarian ekosistem dan menurunkan kualitas keanekaragaman hayati lokal.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_sda}")
    st.markdown(analisis_sda, unsafe_allow_html=True)

# =====================
# KALKULATOR TEV (DINAMIS & KOTAK MENONJOL)
# =====================

elif menu == "Kalkulator TEV":
    st.header("Kalkulator Total Economic Value (TEV)")
    st.write("Simulasi valuasi nilai ekonomi total ekosistem hutan menggunakan slider interaktif untuk mengatur asumsi nilai per hektar.")
    
    pilihan_wilayah = st.selectbox("Pilih Wilayah Analisis Simulasi:", ["Total Provinsi"] + list(df_hutan["Kabupaten/Kota"]))
    
    if pilihan_wilayah == "Total Provinsi":
        luas_analisis = total_luas_provinsi
    else:
        row_kab = df_hutan[df_hutan["Kabupaten/Kota"] == pilihan_wilayah].iloc[0]
        luas_analisis = row_kab["Total Kawasan Hutan (ha)"]
        
    st.info(f"Luas Geografis Hutan Teranalisis: {luas_analisis:,.2f} Hektar")
    
    st.subheader("Geser untuk Mengatur Asumsi Nilai Manfaat Ekosistem (Rp / Hektar / Tahun)")
    col_sl1, col_sl2 = st.columns(2)
    with col_sl1:
        tarif_langsung = st.slider("Asumsi Nilai Guna Langsung (Hasil Kayu Finansial)", min_value=1000, max_value=50000, value=15000, step=500)
        tarif_tidak_langsung = st.slider("Asumsi Nilai Guna Tidak Langsung (Fungsi Karbon & Oksigen)", min_value=1000, max_value=50000, value=20000, step=500)
    with col_sl2:
        tarif_pilihan = st.slider("Asumsi Nilai Pilihan (Keanekaragaman Hayati & Wisata)", min_value=1000, max_value=50000, value=15000, step=500)
        tarif_eksistensi = st.slider("Asumsi Nilai Eksistensi (Warisan Kelestarian Hutan)", min_value=1000, max_value=50000, value=10000, step=500)
        
    nilai_langsung = int(luas_analisis * tarif_langsung)
    nilai_tidak_langsung = int(luas_analisis * tarif_tidak_langsung)
    nilai_pilihan = int(luas_analisis * tarif_pilihan)
    nilai_eksistensi = int(luas_analisis * tarif_eksistensi)
    
    total_tev = nilai_langsung + nilai_tidak_langsung + nilai_pilihan + nilai_eksistensi
    st.metric(label=f"ESTIMASI TOTAL ECONOMIC VALUE (TEV) - {pilihan_wilayah.upper()}", value=f"Rp {total_tev:,.2f}")
    
    st.subheader("Struktur Komparasi Kontribusi Komponen Valuasi TEV")
    df_pie_tev = pd.DataFrame({
        "Komponen Klasifikasi Nilai": ["Guna Langsung", "Guna Tidak Langsung", "Nilai Pilihan", "Nilai Eksistensi"],
        "Aset Valuasi Ekonomi (Rp)": [nilai_langsung, nilai_tidak_langsung, nilai_pilihan, nilai_eksistensi]
    })
    
    fig_pie_tev = px.pie(
        df_pie_tev, 
        values="Aset Valuasi Ekonomi (Rp)", 
        names="Komponen Klasifikasi Nilai", 
        title=f"Persentase Kontribusi Struktur Parameter TEV Kawasan {pilihan_wilayah}",
        color_discrete_sequence=px.colors.sequential.YlGnBu
    )
    st.plotly_chart(fig_pie_tev, use_container_width=True)
    
    nilai_non_pasar = nilai_tidak_langsung + nilai_pilihan + nilai_eksistensi
    persen_non_pasar = (nilai_non_pasar / total_tev) * 100
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_tev = "Menu Kalkulator TEV menerapkan kerangka kerja ekonomi lingkungan untuk mengkuantifikasi nilai moneter total dari ekosistem hutan. Formulasi merangkum nilai guna langsung, nilai tidak langsung, nilai pilihan, dan nilai eksistensi non-pasar."
    
    analisis_tev = f"""
    <div style="background-color: #EFF6FF; padding: 20px; border-left: 6px solid #2563EB; border-radius: 4px;">
        <h4 style="color: #1E40AF; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Hasil simulasi pada kawasan {pilihan_wilayah} membuktikan secara empiris bahwa nilai ekonomi total didominasi oleh fungsi non-pasar yaitu nilai guna tidak langsung, pilihan, dan eksistensi dengan akumulasi nilai 
            <span style="color: #1D4ED8; font-weight: bold;">Rp {nilai_non_pasar:,.2f}</span> atau setara 
            <span style="color: #15803D; font-weight: bold;">{persen_non_pasar:.2f}%</span> dari total nilai ekonomi kawasan. Temuan ini mematahkan argumen bahwa hutan hanya bernilai saat ditebang untuk diambil kayunya yang saat ini dikalkulasi hanya berkontribusi sebesar 
            <span style="color: #B91C1C; font-weight: bold;">Rp {nilai_langsung:,.2f}</span>. Kegagalan dalam menginternalisasi nilai non-pasar ini ke dalam kebijakan pembangunan akan menyebabkan terjadinya eksploitasi lahan yang berlebihan akibat salah urus penilaian aset alam.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_tev}")
    st.markdown(analisis_tev, unsafe_allow_html=True)

# =====================
# ANALISIS TRADE-OFF (DINAMIS & KOTAK MENONJOL)
# =====================

elif menu == "Analisis Trade-Off":
    st.subheader("Simulasi Substitusi Lahan")
    
    st.subheader("Sesuaikan Bobot Prioritas Kebijakan Jangka Panjang")
    bobot_konservasi = st.slider("Fokus Terhadap Kompensasi Ekologis Jangka Panjang (%)", min_value=10, max_value=100, value=95, step=5)
    
    kelayakan_sawit = int(bobot_konservasi * 0.68)
    kelayakan_kayu = int(bobot_konservasi * 0.42)
    
    tradeoff = pd.DataFrame({
        "Skenario": ["Hutan Lestari", "Konversi Sawit", "Eksploitasi Kayu"],
        "Nilai Kelayakan (%)": [bobot_konservasi, kelayakan_sawit, kelayakan_kayu]
    })

    fig = px.bar(
        tradeoff, 
        x="Nilai Kelayakan (%)", 
        y="Skenario", 
        orientation="h", 
        title="Perbandingan Nilai Kelayakan Antar Skenario", 
        color="Skenario",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_tradeoff = "Menu Analisis Trade-Off mensimulasikan dampak pilihan kebijakan ekonomi terhadap keberlanjutan lingkungan. Modul ini membandingkan indeks kelayakan jangka panjang antara skenario konservasi penuh, konversi monokultur kelapa sawit, dan pembalakan kayu."
    
    analisis_tradeoff = f"""
    <div style="background-color: #FFFBEB; padding: 20px; border-left: 6px solid #D97706; border-radius: 4px;">
        <h4 style="color: #92400E; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Saat target kelayakan jangka panjang dipatok pada angka <span style="color: #15803D; font-weight: bold;">{bobot_konservasi}%</span>, 
            skenario konversi kelapa sawit hanya mampu mencapai indeks kelayakan <span style="color: #B45309; font-weight: bold;">{kelayakan_sawit}%</span> 
            dan pembalakan kayu turun drastis ke angka <span style="color: #B91C1C; font-weight: bold;">{kelayakan_kayu}%</span>. Penurunan kelayakan pada opsi ekstraktif dipicu oleh tingginya biaya eksternalitas yang harus ditanggung masyarakat akibat bencana banjir dan hilangnya hilir sirkulasi air bersih. Skenario Hutan Lestari terbukti menghasilkan keberlanjutan ekonomi tertinggi karena menjaga stabilitas modal alam. Transformasi kebijakan dari eksploitasi menuju restorasi terencana merupakan keputusan rasional demi meminimalkan depresiasi kekayaan alam daerah.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_tradeoff}")
    st.markdown(analisis_tradeoff, unsafe_allow_html=True)

# =====================
# PES (DINAMIS & KOTAK MENONJOL)
# =====================

elif menu == "PES":
    st.subheader("Simulasi Imbal Jasa Lingkungan")
    
    karbon_input = st.number_input("Cadangan Karbon (Ton)", value=172000000)
    harga_input = st.number_input("Harga Karbon (Rp/Ton)", value=150000)
    
    hasil = karbon_input * harga_input
    st.metric("Potensi Pendapatan PES", f"Rp {hasil:,.0f}")
    
    st.divider()
    st.subheader("Deskripsi dan Tinjauan Analisis")
    
    deskripsi_pes = "Menu PES (Payment for Ecosystem Services) atau Imbal Jasa Lingkungan mensimulasikan instrumen pasar modern untuk konservasi. Sistem mengalkulasi potensi penerimaan dana segar yang diperoleh daerah melalui skema perdagangan karbon internasional."
    
    analisis_pes = f"""
    <div style="background-color: #FAF5FF; padding: 20px; border-left: 6px solid #7C3AED; border-radius: 4px;">
        <h4 style="color: #5B21B6; margin-top: 0;">Hasil Analisis Ekonomi Lingkungan:</h4>
        <p style="color: #1F2937; line-height: 1.6; margin-bottom: 0;">
            Simulasi menunjukkan potensi penerimaan keuangan daerah yang sangat masif sebesar <span style="color: #1D4ED8; font-weight: bold;">Rp {hasil:,.0f}</span> 
            dari hasil optimalisasi insentif pasar dengan asumsi harga <span style="color: #B45309; font-weight: bold;">Rp {harga_input:,.0f}</span> per ton karbon. Skema PES merubah paradigma konservasi dari pusat pembiayaan pasif menjadi motor penggerak pendapatan daerah yang sangat menguntungkan. Dana kompensasi yang diperoleh dari penciptaan nilai karbon ini harus dialokasikan secara langsung untuk mendanai program pemberdayaan masyarakat adat di sekitar hutan. Pendekatan insentif ekonomi ini menciptakan harmoni antara target pertumbuhan ekonomi makro daerah dan upaya pelestarian kawasan hutan.
        </p>
    </div>
    """
    
    with st.container(border=True):
        st.write(f"**Deskripsi Menu:** {deskripsi_pes}")
    st.markdown(analisis_pes, unsafe_allow_html=True)
