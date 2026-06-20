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
    
    # Proses transformasi data untuk grafik batang
    df_melted = df_kab.melt(id_vars=["Kabupaten/Kota"], var_name="Fungsi Hutan", value_name="Luas (ha)")
    
    # PERBAIKAN: Menggunakan px.bar dan st.plotly_chart, bkan st.bar_chart
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
