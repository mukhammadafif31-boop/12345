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
st.markdown("Dashboard pintar yang bisa membaca, memfilter, dan membuat grafik dari **semua jenis file CSV** secara otomatis!")
st.markdown("---")

# 3. Fitur Upload File
uploaded_file = st.file_uploader("📂 Upload file CSV apa saja di sini:", type=["csv"])

if uploaded_file is not None:
    try:
        # Cek otomatis apakah file menggunakan pemisah (;) atau (,)
        # Membaca baris pertama untuk deteksi delimiter
        sample = uploaded_file.read(2048).decode('utf-8', errors='ignore')
        uploaded_file.seek(0) # Kembalikan posisi baca ke awal
        
        separator = ";" if sample.count(";") > sample.count(",") else ","
        
        # Membaca file CSV
        df = pd.read_csv(uploaded_file, sep=separator, skip_blank_lines=True, on_bad_lines='skip')
        
        # Bersihkan nama kolom dari spasi tidak terlihat
        df.columns = df.columns.str.strip()
        
        st.success(f"✅ Berhasil memuat file! Terdeteksi {len(df)} baris dan {len(df.columns)} kolom.")

        # Pisahkan kolom berdasarkan tipe datanya secara otomatis
        kolom_angka = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_teks = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # 4. Bagian Filter Dinamis di Sidebar
        st.sidebar.header("⚙️ Pengaturan Filter & Grafik")
        
        # Membuat filter otomatis dari kolom teks yang tersedia (maksimal 2 kolom teks pertama agar tidak penuh)
        filtered_df = df.copy()
        if len(kolom_teks) > 0:
            st.sidebar.markdown("### 🔍 Filter Data")
            for col in kolom_teks[:2]: # Mengambil hingga 2 kolom kategori pertama untuk dijadikan filter
                opsi = ["Semua"] + sorted(list(df[col].dropna().unique()))
                pilihan = st.sidebar.selectbox(f"Filter berdasarkan {col}:", opsi)
                if pilihan != "Semua":
                    filtered_df = filtered_df[filtered_df[col] == pilihan]

        # Fitur Pencarian Global
        search_query = st.sidebar.text_input("🔍 Pencarian Kata Kunci:")
        if search_query:
            # Mencari kata kunci di semua kolom teks
            mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            filtered_df = filtered_df[mask]

        # 5. Blok Ringkasan Angka (KPI) Otomatis
        st.markdown("### 📈 Ringkasan Data Saat Ini")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📊 Total Baris Terfilter", value=f"{len(filtered_df)} Data")
        
        # Jika ada kolom angka, tampilkan total dan rata-rata dari kolom angka pertama
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

        # 6. Pembuatan Fitur TAB Layout
        tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Grafik Kustom", "🔬 Analisis Statistik", "📋 Tabel Data & Download"])

        with tab1:
            st.subheader("🛠️ Pengaturan Grafik Anda")
            
            # Cek jika data memenuhi syarat untuk dibuat grafik
            if len(kolom_teks) > 0 and len(kolom_angka) > 0:
                col_sel1, col_sel2 = st.columns(2)
                with col_sel1:
                    sb_x = st.selectbox("Pilih Kolom Kategori (Sumbu X):", kolom_teks)
                with col_sel2:
                    sb_y = st.selectbox("Pilih Kolom Angka/Nilai (Sumbu Y):", kolom_angka)
                
                st.markdown("---")
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.markdown(f"#### 📊 Grafik Batang: Total {sb_y} per {sb_x}")
                    if not filtered_df.empty:
                        chart_data_bar = filtered_df.groupby(sb_x)[sb_y].sum()
                        st.bar_chart(chart_data_bar)
                    else:
                        st.info("Tidak ada data untuk ditampilkan.")

                with col_chart2:
                    st.markdown(f"#### 📈 Grafik Garis: Tren {sb_y} per {sb_x}")
                    if not filtered_df.empty:
                        chart_data_line = filtered_df.groupby(sb_x)[sb_y].sum()
                        st.line_chart(chart_data_line)
                    else:
                        st.info("Tidak ada data untuk ditampilkan.")
            else:
                st.warning("⚠️ File CSV ini tidak memiliki kombinasi kolom teks dan kolom angka yang cukup untuk dibuatkan grafik otomatis.")

        with tab2:
            st.subheader("📊 Ringkasan Statistik Angka")
            if len(kolom_angka) > 0 and not filtered_df.empty:
                stats_df = filtered_df[kolom_angka].describe()
                stats_df.index = ['Total Data', 'Rata-rata', 'Simpangan Baku', 'Nilai Minimum', '25% Kuartil', 'Median (50%)', '75% Kuartil', 'Nilai Maksimum']
                st.dataframe(stats_df, use_container
