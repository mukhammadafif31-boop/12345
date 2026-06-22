import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Advanced Customer Analytics Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bersihkan memori cache lama agar data selalu segar
st.cache_data.clear()

# 2. Header Atas Dashboard dengan Gaya Elegan
st.title("👑 Executive Customer Analytics Dashboard")
st.markdown("Analisis cerdas data pelanggan secara interaktif, cepat, dan mendalam.")
st.markdown("---")

# 3. Fitur Upload File
uploaded_file = st.file_uploader("📂 Silakan Upload File CSV Pelanggan Kamu di Sini:", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca file yang di-upload oleh user
        df = pd.read_csv(uploaded_file, sep=";", skip_blank_lines=True, on_bad_lines='skip')
        
        # Hilangkan spasi tak terlihat pada nama kolom
        df.columns = df.columns.str.strip()
        
        # Konversi data angka agar aman saat dihitung
        if 'Umur' in df.columns:
            df['Umur'] = pd.to_numeric(df['Umur'], errors='coerce').fillna(0).astype(int)
        if 'Nilai Belanja Setahun' in df.columns:
            df['Nilai Belanja Setahun'] = pd.to_numeric(df['Nilai Belanja Setahun'], errors='coerce').fillna(0).astype(int)

        # 4. Bagian Kontrol Filter di Sidebar (Samping)
        st.sidebar.header("⚙️ Pengaturan Filter")
        
        # Filter Jenis Kelamin
        jk_options = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
        selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
        
        # Filter Tipe Residen
        residen_options = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
        selected_residen = st.sidebar.selectbox("Pilih Tipe Residen:", residen_options)
        
        # Filter Profesi
        profesi_options = ["Semua"] + sorted(list(df['Profesi'].dropna().unique()))
        selected_profesi = st.sidebar.selectbox("Pilih Profesi Pelanggan:", profesi_options)

        # Fitur Pencarian Nama Pelanggan langsung dari sidebar
        search_name = st.sidebar.text_input("🔍 Cari Nama Pelanggan:")

        # Terapkan Filter ke Data
        filtered_df = df.copy()
        if selected_jk != "Semua":
            filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == selected_jk]
        if selected_residen != "Semua":
            filtered_df = filtered_df[filtered_df['Tipe Residen'] == selected_residen]
        if selected_profesi != "Semua":
            filtered_df = filtered_df[filtered_df['Profesi'] == selected_profesi]
        if search_name:
            filtered_df = filtered_df[filtered_df['Nama Pelanggan'].str.contains(search_name, case=False, na=False)]

        # 5. Blok Ringkasan Angka (KPI Utama)
        total_pelanggan = len(filtered_df)
        total_belanja = filtered_df['Nilai Belanja Setahun'].sum()
        rata_belanja = filtered_df['Nilai Belanja Setahun'].mean() if total_pelanggan > 0 else 0
        maks_belanja = filtered_df['Nilai Belanja Setahun'].max() if total_pelanggan > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="👤 Total Pelanggan", value=f"{total_pelanggan} Orang")
        with col2:
            st.metric(label="💰 Total Belanja Setahun", value=f"Rp {total_belanja:,.0f}")
        with col3:
            st.metric(label="📈 Rata-rata Belanja", value=f"Rp {rata_belanja:,.0f}")
        with col4:
            st.metric(label="🏆 Belanja Tertinggi", value=f"Rp {maks_belanja:,.0f}")

        st.markdown("---")

        # 6. Pembuatan Fitur TAB untuk merapikan layout web
        tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Utama", "🔬 Analisis Statistik", "📋 Data Terfilter & Download"])

        with tab1:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("🛒 Total Belanja Berdasarkan Profesi")
                if not filtered_df.empty:
                    chart_profesi = filtered_df.groupby('Profesi')['Nilai Belanja Setahun'].sum()
                    st.bar_chart(chart_profesi)
                else:
                    st.info("Tidak ada data untuk filter ini.")

            with col_chart2:
                st.subheader("🎂 Jumlah Pelanggan Berdasarkan Rentang Umur")
                if not filtered_df.empty:
                    chart_umur = filtered_df.groupby('Umur').size()
                    st.bar_chart(chart_umur)
                else:
                    st.info("Tidak ada data untuk filter ini.")
            
            st.markdown("---")
            st.subheader("🏠 Kontribusi Nilai Belanja Berdasarkan Tipe Residen")
            if not filtered_df.empty:
                chart_residen = filtered_df.groupby('Tipe Residen')['Nilai Belanja Setahun'].sum()
                st.line_chart(chart_residen)

        with tab2:
            st.subheader("📊 Ringkasan Statistik Data Terfilter")
            if not filtered_df.empty:
                # Membuat ringkasan statistik yang mudah dibaca untuk umur dan nilai belanja
                stats_df = filtered_df[['Umur', 'Nilai Belanja Setahun']].describe()
                stats_df.index = ['Total Data', 'Rata-rata', 'Simpangan Baku', 'Nilai Minimum', '25% Kuartil', 'Median (50%)', '75% Kuartil', 'Nilai Maksimum']
                st.dataframe(stats_df, use_container_width=True)
            else:
                st.info("Tidak ada data untuk dianalisis.")

        with tab3:
            st.subheader("📋 Tabel Data Pelanggan Aktif")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            # Fitur Ekspor Data Ke CSV Berdasarkan Filter Saat Ini
            if not filtered_df.empty:
                csv_data = filtered_df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="📥 Download Data Terfilter (CSV)",
                    data=csv_data,
                    file_name="data_pelanggan_terfilter.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"⚠️ Terjadi gangguan saat membaca file: {e}")
else:
    # Tampilan awal jika user belum upload file apa pun
    st.info("💡 Tolong upload file **data_pelanggan (2).csv** kamu pada tombol di atas terlebih dahulu untuk memunculkan dashboard eksekutif yang keren ini!")
