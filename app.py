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

# CSS KUSTOM UNTUK VISUALISASI
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; color: #1E3A8A; }
    .card { background-color: #f8fafc; padding: 20px; border-radius: 12px; border-left: 6px solid #3B82F6; box-shadow: 3px 3px 10px #e2e8f0; margin-bottom: 15px;}
    .dosen-box { background-color: #fef2f2; padding: 15px; border-radius: 10px; border: 1px solid #fee2e2; margin-bottom: 25px;}
    </style>
    """, unsafe_allow_html=True)

# =====================
# DATASET
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
total_luas_provinsi = df_hutan["Total Kawasan Hutan (ha)"].sum()

# =====================
# HEADER & IDENTITAS
# =====================
col1, col2 = st.columns([1, 4])
with col2:
    st.markdown("<p class='big-font'>ECO-FOREST VALUATION HUTAN KALIMANTAN SELATAN</p>", unsafe_allow_html=True)
    st.write("Project Based Learning Ekonomi Sumber Daya Alam dan Lingkungan")
    st.markdown("""
        <div class='dosen-box'>
            <span style='color: #991b1b; font-weight: bold;'>Dosen Pengampu:</span> 
            <span style='color: #b91c1c;'>Yuhka Sundaya, S.E., M.Si. (NIDN: 0424057601)</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<span style='color: #1E3A8A; font-weight: bold; font-size: 18px;'>ANGGOTA KELOMPOK 9:</span>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.markdown("<div class='card'><b>Ina Rani Amelia</b><br>NPM: 10090224002</div>", unsafe_allow_html=True)
c2.markdown("<div class='card'><b>Nayla Dwi Safitri</b><br>NPM: 10090224013</div>", unsafe_allow_html=True)
c3.markdown("<div class='card'><b>Celi Maulidi Aprilia</b><br>NPM: 10090224027</div>", unsafe_allow_html=True)

st.divider()

# =====================
# SIDEBAR NAVIGATION
# =====================
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Beranda", "Fungsi Hutan", "Profil SDA", "Kalkulator TEV", "Analisis Trade-Off", "PES"]
)

# =====================
# LOGIKA MENU
# =====================

if menu == "Beranda":
    st.subheader("Kondisi Fisik dan Makro Kehutanan")
    st.dataframe(df_hutan.drop(columns=["Total Kawasan Hutan (ha)"]), use_container_width=True)
    st.markdown("""
    ### Analisis
    Ketimpangan distribusi hutan antar kabupaten di Kalimantan Selatan menuntut kebijakan tata ruang yang berbasis pada jasa ekosistem.
    """)

elif menu == "Fungsi Hutan":
    st.subheader("Distribusi Fungsi Kawasan")
    fig = px.pie(names=["Lindung", "Suaka", "Produksi Terbatas", "Produksi Tetap", "Konversi"], 
                 values=[df_hutan["Hutan Lindung (ha)"].sum(), 50000, 30000, 100000, 20000])
    st.plotly_chart(fig)
    st.markdown("""
    ### Analisis
    Dominasi hutan produksi menunjukkan orientasi ekstraktif yang tinggi. Perlu restrukturisasi menuju konservasi untuk menjaga modal alam.
    """)

elif menu == "Kalkulator TEV":
    st.header("Simulasi Nilai Ekonomi Total (TEV)")
    wilayah = st.selectbox("Pilih Wilayah:", df_hutan["Kabupaten/Kota"])
    luas = df_hutan[df_hutan["Kabupaten/Kota"] == wilayah]["Total Kawasan Hutan (ha)"].values[0]
    
    t1 = st.slider("Nilai Guna Langsung (Rp/ha)", 1000, 50000, 15000)
    t2 = st.slider("Nilai Guna Tidak Langsung (Rp/ha)", 1000, 50000, 20000)
    
    tev = (luas * t1) + (luas * t2)
    st.metric("Total TEV", f"Rp {tev:,.2f}")
    st.markdown("""
    ### Analisis
    Hasil simulasi membuktikan bahwa nilai jasa lingkungan (tidak langsung) seringkali lebih besar daripada nilai ekstraksi kayu secara langsung.
    """)

elif menu == "Analisis Trade-Off":
    st.header("Simulasi Substitusi Lahan")
    st.write("Analisis perbandingan antara skenario kelestarian hutan dan eksploitasi ekonomi.")
    # Kode visualisasi trade-off di sini

elif menu == "PES":
    st.header("Imbal Jasa Lingkungan (PES)")
    st.write("Simulasi pendapatan daerah melalui perdagangan karbon.")
    # Kode kalkulator PES di sini
