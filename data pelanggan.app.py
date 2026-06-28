import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Premium Customer Business Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bersihkan cache lama agar data selalu fresh
st.cache_data.clear()

# 2. Header Atas Dashboard Eksekutif
st.title("💎 Premium Customer Business Intelligence Dashboard")
st.markdown("Analisis visual dan statistik mendalam berbasis data pelanggan secara instan dan interaktif.")
st.markdown("---")

# 3. Fitur Unggah File CSV
uploaded_file = st.file_uploader(
    "📂 Seret atau pilih file 'data_pelanggan (2).csv' kamu di sini:", 
    type=["csv"]
)

if uploaded_file is not None:
    try:
        # Deteksi otomatis pembatas karakter (delimiter) semikolon (;) atau koma (,)
        sample = uploaded_file.read(2048).decode('utf-8', errors='ignore')
        uploaded_file.seek(0)
        separator = ";" if sample.count(";") > sample.count(",") else ","
        
        # Baca dataset
        df = pd.read_csv(
            uploaded_file, 
            sep=separator, 
            skip_blank_lines=True, 
            on_bad_lines='skip'
        )
        
        # Bersihkan nama kolom dari spasi tidak terlihat
        df.columns = df.columns.str.strip()
        
        st.success(f"📊 Berhasil Memuat Data: {len(df)} Pelanggan Terdaftar.")

        # Konversi data angka agar aman saat dihitung
        if 'Umur' in df.columns:
            df['Umur'] = pd.to_numeric(df['Umur'], errors='coerce').fillna(0).astype(int)
        if 'Nilai Belanja Setahun' in df.columns:
            df['Nilai Belanja Setahun'] = pd.to_numeric(df['Nilai Belanja Setahun'], errors='coerce').fillna(0).astype(int)

        # Deteksi tipe kolom secara otomatis untuk kebutuhan visualisasi kustom
        kolom_angka = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_teks = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # 4. Pengaturan Menu Kontrol di Sidebar
        st.sidebar.header("⚙️ Menu Kontrol & Filter")
        
        filtered_df = df.copy()
        
        # Filter dinamis menggunakan kolom yang ada di data kamu
        if 'Jenis Kelamin' in df.columns:
            opsi_jk = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
            pilihan_jk = st.sidebar.selectbox("Filter Jenis Kelamin:", opsi_jk)
            if pilihan_jk != "Semua":
                filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == pilihan_jk]
                
        if 'Tipe Residen' in df.columns:
            opsi_residen = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
            pilihan_residen = st.sidebar.selectbox("Filter Tipe Residen:", opsi_residen)
            if pilihan_residen != "Semua":
                filtered_df = filtered_df[filtered_df['Tipe Residen'] == pilihan_residen]

        # Fitur Pencarian Global Kata Kunci (Bisa cari nama, profesi, dll)
        st.sidebar.markdown("### 📝 Pencarian Pelanggan")
        search_query = st.sidebar.text_input("Cari Nama atau Kata Kunci:")
        if search_query:
            mask = filtered_df.apply(
                lambda r: r.astype(str).str.contains(search_query, case=False).any(), 
                axis=1
            )
            filtered_df = filtered_df[mask]

        # 5. Blok Metrik Utama (KPI Korporat)
        st.markdown("### 📈 Ringkasan Eksekutif")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="📊 Total Pelanggan", value=f"{len(filtered_df)} Orang")
        
        if 'Nilai Belanja Setahun' in filtered_df.columns:
            with col2:
                total_nilai = filtered_df['Nilai Belanja Setahun'].sum()
                st.metric(label="💰 Total Belanja Terfilter", value=f"Rp {total_nilai:,.0f}")
            with col3:
                rata_nilai = filtered_df['Nilai Belanja Setahun'].mean() if len(filtered_df) > 0 else 0
                st.metric(label="📈 Rata-rata Belanja", value=f"Rp {rata_nilai:,.0f}")
            with col4:
                maks_nilai = filtered_df['Nilai Belanja Setahun'].max() if len(filtered_df) > 0 else 0
                st.metric(label="🏆 Belanja Tertinggi", value=f"Rp {maks_nilai:,.0f}")
        else:
            with col2: st.metric(label="💰 Total Nilai", value="0")
            with col3: st.metric(label="📈 Rata-rata", value="0")
            with col4: st.metric(label="🏆 Nilai Maksimal", value="0")

        st.markdown("---")

        # 6. Tata Letak Menu Menggunakan Tab Kebanggaan Streamlit
        tab1, tab2, tab3 = st.tabs([
            "📊 Visualisasi Grafik", 
            "🔬 Analisis Statistik Deskriptif", 
            "📋 Inspeksi Data & Ekspor"
        ])

        with tab1:
            st.subheader("🛠️ Konfigurasi Grafik Kustom")
            if len(kolom_teks) > 0 and len(kolom_angka) > 0:
                col_sel1, col_sel2, col_sel3 = st.columns(3)
                with col_sel1:
                    # Otomatis merekomendasikan 'Profesi' atau teks lain
                    idx_x = kolom_teks.index('Profesi') if 'Profesi' in kolom_teks else 0
                    sb_x = st.selectbox("Sumbu X (Kategori):", kolom_teks, index=idx_x)
                with col_sel2:
                    # Otomatis merekomendasikan 'Nilai Belanja Setahun' atau angka lain
                    idx_y = kolom_angka.index('Nilai Belanja Setahun') if 'Nilai Belanja Setahun' in kolom_angka else 0
                    sb_y = st.selectbox("Sumbu Y (Nilai Ukur):", kolom_angka, index=idx_y)
                with col_sel3:
                    tipe_hitung = st.radio("Metode Perhitungan:", ["Total Keseluruhan (Sum)", "Rata-rata (Mean)"])
                
                st.markdown("---")
                
                if not filtered_df.empty:
                    if tipe_hitung == "Total Keseluruhan (Sum)":
                        chart_data = filtered_df.groupby(sb_x)[sb_y].sum()
                    else:
                        chart_data = filtered_df.groupby(sb_x)[sb_y].mean()
                        
                    col_chart1, col_chart2 = st.columns(2)
                    with col_chart1:
                        st.markdown(f"#### 📊 Grafik Batang ({tipe_hitung})")
                        st.bar_chart(chart_data)
                    with col_chart2:
                        st.markdown(f"#### 📈 Grafik Area Tren ({tipe_hitung})")
                        st.area_chart(chart_data)
                else:
                    st.info("Tidak ada data untuk direpresentasikan ke dalam grafik.")
            else:
                st.warning("⚠️ File ini kekurangan kombinasi data teks dan angka untuk digambar secara otomatis.")

        with tab2:
            st.subheader("🔬 Analisis Ringkasan Matematika & Statistik")
            if len(kolom_angka) > 0 and not filtered_df.empty:
                stats_df = filtered_df[kolom_angka].describe()
                stats_df.index = [
                    'Jumlah Data Resmi', 'Rata-rata Sistem', 'Simpangan Baku', 
                    'Nilai Minimum', 'Kuartil Bawah (25%)', 'Nilai Tengah (Median)', 
                    'Kuartil Atas (75%)', 'Nilai Maksimum'
                ]
                st.dataframe(
                    stats_df, 
                    use_container_width=True
                )
            else:
                st.info("Tidak ditemukan kolom angka untuk menghasilkan perhitungan statistik.")

        with tab3:
            st.subheader("📋 Manajemen Tampilan Tabel Data")
            
            # Memilih kolom secara dinamis agar tabel rapi dan tidak terlalu lebar
            kolom_terpilih = st.multiselect(
                "Pilih kolom yang ingin ditampilkan pada tabel (Kosongkan untuk melihat semua):",
                options=df.columns.tolist(),
                default=df.columns.tolist()[:6]
            )
            
            tabel_tampil = filtered_df[kolom_terpilih] if kolom_terpilih else filtered_df
            
            st.dataframe(
                tabel_tampil, 
                use_container_width=True, 
                hide_index=True
            )
            
            # Tombol ekspor data yang sudah difilter
            if not filtered_df.empty:
                st.markdown("---")
                csv_data = filtered_df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="📥 Unduh Hasil Analisis & Filter Ini (Format CSV)",
                    data=csv_data,
                    file_name="analisis_data_pelanggan.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"⚠️ Terjadi hambatan saat memproses file CSV: {e}")
else:
    st.info("💡 Selamat Datang! Silakan unggah file **data_pelanggan (2).csv** kamu menggunakan tombol di atas untuk melihat visualisasi dashboard premium.")
