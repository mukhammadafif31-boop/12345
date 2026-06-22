import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Universal Business Intelligence Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bersihkan cache lama agar data selalu diperbarui jika ganti file
st.cache_data.clear()

# 2. Header Dashboard Eksekutif
st.title("🚀 Universal Business Intelligence Dashboard")
st.markdown("Ubah file CSV apa saja menjadi visualisasi interaktif dan analisis statistik mendalam secara instan.")
st.markdown("---")

# 3. Fitur Unggah File CSV
uploaded_file = st.file_uploader(
    "📂 Seret atau pilih file CSV kamu di sini:", 
    type=["csv"]
)

if uploaded_file is not None:
    try:
        # Cek otomatis karakter pemisah (delimiter) koma (,) atau semikolon (;)
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
        
        st.success(f"📊 Berhasil Memuat Data: {len(df)} Baris & {len(df.columns)} Kolom Terdeteksi.")

        # Deteksi tipe kolom secara otomatis
        kolom_angka = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_teks = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # 4. Pengaturan Menu Kontrol di Sidebar
        st.sidebar.header("⚙️ Menu Kontrol & Filter")
        
        filtered_df = df.copy()
        
        # Filter dinamis untuk 2 kolom teks pertama agar sidebar tetap rapi
        if len(kolom_teks) > 0:
            st.sidebar.markdown("### 🔍 Filter Kategori")
            for col in kolom_teks[:2]:
                opsi = ["Semua"] + sorted(list(df[col].dropna().unique()))
                pilihan = st.sidebar.selectbox(f"Berdasarkan {col}:", opsi)
                if pilihan != "Semua":
                    filtered_df = filtered_df[filtered_df[col] == pilihan]

        # Fitur Pencarian Global Kata Kunci
        st.sidebar.markdown("### 📝 Pencarian Spesifik")
        search_query = st.sidebar.text_input("Cari Kata Kunci Apa Saja:")
        if search_query:
            mask = filtered_df.apply(
                lambda r: r.astype(str).str.contains(search_query, case=False).any(), 
                axis=1
            )
            filtered_df = filtered_df[mask]

        # 5. Blok Metrik Utama (KPI Ringsan)
        st.markdown("### 📈 Ringkasan Eksekutif")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="📊 Total Data Terfilter", value=f"{len(filtered_df)} Baris")
        
        if len(kolom_angka) > 0:
            kolom_kpi = kolom_angka[0]
            with col2:
                total_nilai = filtered_df[kolom_kpi].sum()
                st.metric(label=f"💰 Total {kolom_kpi}", value=f"{total_nilai:,.0f}")
            with col3:
                rata_nilai = filtered_df[kolom_kpi].mean() if len(filtered_df) > 0 else 0
                st.metric(label=f"📈 Rata-rata {kolom_kpi}", value=f"{rata_nilai:,.0f}")
            with col4:
                maks_nilai = filtered_df[kolom_kpi].max() if len(filtered_df) > 0 else 0
                st.metric(label=f"🏆 {kolom_kpi} Tertinggi", value=f"{maks_nilai:,.0f}")
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
            st.subheader("🛠️ Pengaturan & Konfigurasi Grafik Kustom")
            if len(kolom_teks) > 0 and len(kolom_angka) > 0:
                col_sel1, col_sel2, col_sel3 = st.columns(3)
                with col_sel1:
                    sb_x = st.selectbox("Pilih Sumbu X (Kategori Teks):", kolom_teks)
                with col_sel2:
                    sb_y = st.selectbox("Pilih Sumbu Y (Nilai Angka):", kolom_angka)
                with col_sel3:
                    tipe_hitung = st.radio("Metode Perhitungan Grafik:", ["Total Keseluruhan (Sum)", "Rata-rata (Mean)"])
                
                st.markdown("---")
                
                # Proses kalkulasi data grafik sesuai metode perhitungan terpilih
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
                st.info("Tidak ditemukan kolom angka untuk menghasilkan perhitungan statistik deskriptif.")

        with tab3:
            st.subheader("📋 Manajemen Tampilan Tabel Data")
            
            # Fitur keren: Memilih kolom secara dinamis untuk menyembunyikan data sensitif/tidak penting
            kolom_terpilih = st.multiselect(
                "Pilih kolom yang ingin ditampilkan pada tabel (Kosongkan untuk melihat semua):",
                options=df.columns.tolist(),
                default=df.columns.tolist()[:5] # Tampilkan 5 kolom pertama secara default agar rapi
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
                    label="📥 Unduh Hasil Analisis & Filter (Format CSV)",
                    data=csv_data,
                    file_name="analisis_dashboard_eksekutif.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"⚠️ Terjadi hambatan saat meraba data file CSV: {e}")
else:
    st.info("💡 Selamat Datang! Silakan unggah file CSV apa saja menggunakan tombol di atas untuk memulai analisis cerdas.")
