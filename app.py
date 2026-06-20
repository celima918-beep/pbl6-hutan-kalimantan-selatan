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

elif menu == "Profil SDA":
    st.header("Profil Sumber Daya Alam Kehutanan")
    
    # -------------------------------------------------------------
    # BAGIAN 1: KEANEKARAGAMAN HAYATI
    # -------------------------------------------------------------
    st.subheader("1. Keanekaragaman Hayati (Biodiversitas)")
    
    df_bio = pd.DataFrame({
        "Kategori": ["Flora", "Fauna"],
        "Jumlah Kerapatan Spesies": [3000, 500]
    })
    
    col_bio1, col_bio2 = st.columns([1, 2])
    with col_bio1:
        st.dataframe(df_bio, use_container_width=True)
    with col_bio2:
        fig_bio = px.bar(df_bio, x="Kategori", y="Jumlah Kerapatan Spesies", color="Kategori",
                         title="Perbandingan Kerapatan Spesies Kehutanan",
                         color_discrete_map={"Flora": "#1abc9c", "Fauna": "#ff7f50"})
        st.plotly_chart(fig_bio, use_container_width=True)
        
    st.markdown("""
    **Keterangan Grafik 1. Keanekaragaman Hayati (Biodiversitas)**
    * **Data Spesies Terdata:** Hutan Kalimantan Selatan mencatatkan total kerapatan sebanyak **3.000 jenis spesies Flora** (Tumbuhan) dan **500 jenis spesies Fauna** (Hewan).
    * **Perbandingan Visual:** Grafik batang (*bar chart*) menunjukkan dominasi mutlak volume komponen Flora yang mencapai puncak indeks angka 3.000, berbanding kontras dengan komponen Fauna yang berada di skala 500.
    * **Rasio Kerapatan:** Perbandingan biodiversitas bernilai **6 : 1**, mengindikasikan varietas flora terdata enam kali lipat lebih padat dan beragam dibandingkan dengan varietas fauna di kawasan tersebut.
    * **Kesimpulan Data:** Struktur sebaran ini menegaskan karakteristik ekosistem kehutanan Kalimantan Selatan sebagai wilayah *mega-biodiversity* yang berfungsi utama sebagai penyangga plasma nutfah vegetasi sekaligus habitat esensial bagi ratusan komoditas satwa.
    """)
    
    st.divider()
    
    # -------------------------------------------------------------
    # BAGIAN 2: CADANGAN KARBON
    # -------------------------------------------------------------
    st.subheader("2. Kapasitas Volumetrik Cadangan Karbon")
    
    df_karbon = pd.DataFrame({
        "Kategori Parameter": ["Cadangan Karbon Tetap", "Serapan Karbon Tahunan"],
        "Volume (Ton)": [172000000, 6400000]
    })
    
    col_karb1, col_karb2 = st.columns([1, 2])
    with col_karb1:
        st.dataframe(df_karbon, use_container_width=True)
    with col_karb2:
        fig_karbon = px.pie(df_karbon, names="Kategori Parameter", values="Volume (Ton)",
                            title="Proporsi Distribusi Aspek Karbon",
                            color_discrete_sequence=["#1f4e5b", "#008080"])
        st.plotly_chart(fig_karbon, use_container_width=True)
        
    st.markdown("""
    **Keterangan Grafik 2. Kapasitas Volumetrik Cadangan Karbon**
    * **Rincian Data Parameter:** * **Cadangan Karbon Tetap:** Berjumlah **172.000.000 Ton**.
        * **Serapan Karbon Tahunan:** Berjumlah **6.400.000 Ton**.
    * **Proporsi Distribusi Aspek Karbon:** Berdasarkan grafik lingkaran (*pie chart*), porsi terbesar didominasi mutlak oleh **Cadangan Karbon Tetap** dengan persentase mencapai **96,4%**. Sementara itu, **Serapan Karbon Tahunan** hanya menyumbang porsi kecil sebesar **3,59%**.
    * **Kesimpulan Data:** Data ini menunjukkan bahwa ekosistem hutan Kalimantan Selatan berfungsi sangat krusial sebagai gudang penyimpanan utama karbon (*carbon stock storage*) berskala masif, di mana cadangan statis yang tersimpan jauh lebih besar dibandingkan dengan kapasitas penyerapan dinamis tahunannya.
    """)
    
    st.divider()
    
    # -------------------------------------------------------------
    # BAGIAN 3: JASA LINGKUNGAN
    # -------------------------------------------------------------
    st.subheader("3. Jasa Lingkungan Wisata Rekreasi Alam")
    
    df_wisata = pd.DataFrame({
        "Destinasi": ["Loksado", "Tahura Sultan Adam", "Pegunungan Meratus", "Air Terjun Haratai", "Pulau Kembang"],
        "Kawasan Administratif": ["Hulu Sungai Selatan", "Banjar/Banjarbaru", "Hulu Sungai Tengah", "Hulu Sungai Selatan", "Barito Kuala"]
    })
    
    st.dataframe(df_wisata, use_container_width=True)
    
    st.markdown("""
    **Keterangan Tabel 3. Jasa Lingkungan Wisata Rekreasi Alam**
    Tabel di atas memuat sebaran destinasi wisata rekreasi alam potensial yang memanfaatkan jasa lingkungan hutan di Provinsi Kalimantan Selatan beserta wilayah administratifnya:
    * **Loksado:** Berada di wilayah administratif **Hulu Sungai Selatan**.
    * **Tahura Sultan Adam:** Berada di wilayah administratif **Banjar/Banjarbaru**.
    * **Pegunungan Meratus:** Berada di wilayah administratif **Hulu Sungai Tengah**.
    * **Air Terjun Haratai:** Berada di wilayah administratif **Hulu Sungai Selatan**.
    * **Pulau Kembang:** Berada di wilayah administratif **Barito Kuala**.

    *Kesimpulan Data:* Kabupaten Hulu Sungai Selatan tercatat memiliki keterwakilan destinasi paling banyak pada tabel ini (Loksado dan Air Terjun Haratai), menunjukkan wilayah tersebut memiliki potensi pemanfaatan jasa lingkungan berbasis ekowisata alam yang cukup dominan di Kalimantan Selatan.
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

elif menu == "PES":
    st.header("Imbal Jasa Lingkungan (PES)")
    st.write("Simulasi pendapatan daerah melalui perdagangan karbon.")
