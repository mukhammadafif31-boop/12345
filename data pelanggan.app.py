import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Universal CSV Analytics Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.cache_data.clear()

# 2. Header Atas Dashboard
st.title("🔮 Universal CSV Analytics Dashboard")
st.markdown("Dashboard pintar untuk memproses dan menganalisis **semua jenis file CSV** secara otomatis!")
st.markdown("---")

# 3. Fitur Upload File
uploaded_file = st.file_uploader(
    "📂 Upload file CSV apa saja di sini:", 
    type=["csv"]
)

if uploaded_file is not None:
    try:
        # Deteksi otomatis pembatas separator (koma atau semikolon)
        sample = uploaded_file.read(2048).decode('utf-8', errors='ignore')
        uploaded_file.seek(0)
        separator = ";" if sample.count(";") > sample.count(",") else ","
        
        # Membaca file CSV pelapor
        df = pd.read_csv(
            uploaded_file, 
            sep=separator, 
            skip_blank_lines=True, 
            on_bad_lines='skip'
        )
        
        # Bersihkan spasi tak terlihat pada nama kolom
        df.columns = df.columns.str.strip()
        
        st.success(f"✅ Berhasil memuat file! Terdeteksi {len(df)} baris.")

        # Pisahkan kolom berdasarkan tipe data otomatis
        kolom_angka = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_teks = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # 4. Bagian Filter Dinamis di Sidebar
        st.sidebar.header("⚙️ Pengaturan Filter")
        
        filtered_df = df.copy()
        if len(kolom_teks) > 0:
            for col in kolom_teks[:2]:
                opsi = ["Semua"] + sorted(list(df[col].dropna().unique()))
                pilihan = st.sidebar.selectbox(f"Filter {col}:", opsi)
                if pilihan != "Semua":
                    filtered_df = filtered_df[filtered_df[col] == pilihan]

        # Fitur Pencarian Global
        search_query = st.sidebar.text_input("🔍 Pencarian Kata Kunci:")
        if search_query:
            mask = filtered_df.apply(
                lambda r: r.astype(str).str.contains(search_query, case=False).any(), 
                axis=1
            )
            filtered_df = filtered_df[mask]

        # 5. Blok Ringkasan Angka (KPI)
        st.markdown("### 📈 Ringkasan Data Saat Ini")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📊 Total Baris", value=f"{len(filtered_df)} Data")
        
        if len(kolom_angka) > 0:
            kolom_kpi = kolom_angka[0]
            with col2:
                total_nilai = filtered_df[kolom_kpi].sum()
                st.metric(label=f"💰 Total {kolom_kpi}", value=f"{total_nilai:,.0f}")
            with col3:
                rata_nilai = filtered_df[kolom_kpi].mean() if len(filtered_df) > 0 else 0
                st.metric(label=f"📈 Rata-rata {kolom_kpi}", value=f"{rata_nilai:,.0f}")
        else:
            with col2:
                st.metric(label="💰 Total Kolom Angka", value="0")
            with col3:
                st.metric(label="📈 Rata-rata Kolom Angka", value="0")

        st.markdown("---")

        # 6. Tab Tampilan Menu Web
        tab1, tab2, tab3 = st.tabs([
            "📊 Visualisasi Grafik", 
            "🔬 Analisis Statistik", 
            "📋 Data Terfilter & Download"
        ])

        with tab1:
            st.subheader("🛠️ Pengaturan Grafik")
            if len(kolom_teks) > 0 and len(kolom_angka) > 0:
                col_sel1, col_sel2 = st.columns(2)
                with col_sel1:
                    sb_x = st.selectbox("Pilih Sumbu X (Teks):", kolom_teks)
                with col_sel2:
                    sb_y = st.selectbox("Pilih Sumbu Y (Angka):", kolom_angka)
                
                st.markdown("---")
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.markdown(f"#### 📊 Grafik Batang {sb_y} per {sb_x}")
                    if not filtered_df.empty:
                        chart_bar = filtered_df.groupby(sb_x)[sb_y].sum()
                        st.bar_chart(chart_bar)
                    else:
                        st.info("Data kosong.")

                with col_chart2:
                    st.markdown(f"#### 📈 Grafik Garis {sb_y} per {sb_x}")
                    if not filtered_df.empty:
                        chart_line = filtered_df.groupby(sb_x)[sb_y].sum()
                        st.line_chart(chart_line)
                    else:
                        st.info("Data kosong.")
            else:
                st.warning("⚠️ File ini tidak memiliki kombinasi kolom teks dan angka yang pas untuk grafik.")

        with tab2:
            st.subheader("📊 Ringkasan Analisis Statistik")
            if len(kolom_angka) > 0 and not filtered_df.empty:
                stats_df = filtered_df[kolom_angka].describe()
                stats_df.index = [
                    'Total Data', 'Rata-rata', 'Simpangan Baku', 
                    'Nilai Minimum', '25% Kuartil', 'Median (50%)', 
                    '75% Kuartil', 'Nilai Maksimum'
                ]
                # Baris di bawah ini sengaja dipotong pendek ke bawah agar tidak terputus lagi
                st.dataframe(
                    stats_df, 
                    use_container_width=True
                )
            else:
                st.info("Tidak ada kolom angka untuk dianalisis.")

        with tab3:
            st.subheader("📋 Tabel Data Aktif")
            st.dataframe(
                filtered_df, 
                use_container_width=True, 
                hide_index=True
            )
            
            if not filtered_df.empty:
                csv_data = filtered_df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="📥 Download Hasil Filter (CSV)",
                    data=csv_data,
                    file_name="hasil_analisis.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan pemrosesan file: {e}")
else:
    st.info("💡 Silakan upload file CSV apa saja untuk memunculkan dashboard otomatis!")
