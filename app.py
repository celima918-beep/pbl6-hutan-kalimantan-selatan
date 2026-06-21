# =====================
# KALKULATOR TEV
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
