import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paksa bersihkan cache lama biar segar kembali
st.cache_data.clear()

# 2. Fungsi Membaca Data (Sangat Aman & Ringan)
def load_data():
    # Membaca file dengan pemisah semikolon (;) sesuai struktur aslinya
    df = pd.read_csv("data_pelanggan (2).csv", sep=";", skip_blank_lines=True, on_bad_lines='skip')
    # Hilangkan spasi tak terlihat pada nama kolom
    df.columns = df.columns.str.strip()
    
    # Konversi data angka agar tidak eror saat dihitung
    if 'Umur' in df.columns:
        df['Umur'] = pd.to_numeric(df['Umur'], errors='coerce').fillna(0).astype(int)
    if 'Nilai Belanja Setahun' in df.columns:
        df['Nilai Belanja Setahun'] = pd.to_numeric(df['Nilai Belanja Setahun'], errors='coerce').fillna(0).astype(int)
    return df

try:
    df = load_data()

    # 3. Bagian Kontrol Filter di Sidebar (Samping)
    st.sidebar.header("⚙️ Filter Data")
    
    # Filter Jenis Kelamin
    jk_options = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
    selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
    
    # Filter Tipe Residen
    residen_options = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
    selected_residen = st.sidebar.selectbox("Pilih Tipe Residen:", residen_options)

    # Terapkan Filter ke Data
    filtered_df = df.copy()
    if selected_jk != "Semua":
        filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == selected_jk]
    if selected_residen != "Semua":
        filtered_df = filtered_df[filtered_df['Tipe Residen'] == selected_residen]

    # 4. Bagian Atas Dashboard (Header)
    st.title("📊 Dashboard Analisis Pelanggan")
    st.markdown("Dashboard interaktif ringan, cepat, dan anti-eror untuk memantau performa penjualan.")
    st.markdown("---")

    # 5. Blok Ringkasan Angka (KPI)
    total_pelanggan = len(filtered_df)
    total_belanja = filtered_df['Nilai Belanja Setahun'].sum()
    rata_belanja = filtered_df['Nilai Belanja Setahun'].mean() if total_pelanggan > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👤 Total Pelanggan", value=f"{total_pelanggan} Orang")
    with col2:
        st.metric(label="💰 Total Belanja Setahun", value=f"Rp {total_belanja:,.0f}")
    with col3:
        st.metric(label="📈 Rata-rata Belanja", value=f"Rp {rata_belanja:,.0f}")

    st.markdown("---")

    # 6. Baris Visualisasi Grafik Bawaan (Anti-Eror Module)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("🛒 Total Belanja Berdasarkan Profesi")
        if not filtered_df.empty:
            # Mengelompokkan data profesi
            chart_profesi = filtered_df.groupby('Profesi')['Nilai Belanja Setahun'].sum()
            st.bar_chart(chart_profesi)
        else:
            st.info("Tidak ada data untuk filter ini.")

    with col_chart2:
        st.subheader("🎂 Jumlah Pelanggan Berdasarkan Umur")
        if not filtered_df.empty:
            # Mengelompokkan jumlah orang per umur
            chart_umur = filtered_df.groupby('Umur').size()
            st.bar_chart(chart_umur)
        else:
            st.info("Tidak ada data untuk filter ini.")

    st.markdown("---")

    # 7. Baris Tabel Data Utama
    st.subheader("📋 Tabel Data Pelanggan Terfilter")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("❌ File **'data_pelanggan (2).csv'** tidak ditemukan! Pastikan file diletakkan di tempat yang sama dengan script python ini.")
except Exception as e:
    st.error(f"⚠️ Terjadi gangguan: {e}")
