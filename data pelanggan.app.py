import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PENTING: Paksa hapus cache lama yang rusak agar tidak menimbun error
st.cache_data.clear()

# 2. Fungsi Load Data yang Kebal Error & Toleran terhadap data aneh
def load_data():
    # Menggunakan on_bad_lines='skip' agar jika ada baris rusak di CSV otomatis dilewati tanpa membuat aplikasi crash
    df = pd.read_csv(
        "data_pelanggan (2).csv", 
        sep=";", 
        skip_blank_lines=True,
        on_bad_lines='skip'
    )
    
    # Bersihkan nama kolom dari spasi tidak terlihat
    df.columns = df.columns.str.strip()
    
    # Ubah tipe data kolom angka agar aman
    if 'Umur' in df.columns:
        df['Umur'] = pd.to_numeric(df['Umur'], errors='coerce').fillna(0).astype(int)
    if 'Nilai Belanja Setahun' in df.columns:
        df['Nilai Belanja Setahun'] = pd.to_numeric(df['Nilai Belanja Setahun'], errors='coerce').fillna(0).astype(int)
        
    return df

try:
    df = load_data()

    # Cek apakah kolom wajib ada di file CSV
    kolom_wajib = ['Jenis Kelamin', 'Tipe Residen', 'Umur', 'Profesi', 'Nilai Belanja Setahun']
    missing_cols = [col for col in kolom_wajib if col not in df.columns]
    
    if missing_cols:
        st.error(f"⚠️ Kolom berikut tidak ditemukan di file CSV kamu: {missing_cols}")
        st.info(f"Kolom yang terdeteksi di dalam file kamu saat ini adalah: {list(df.columns)}")
    else:
        # 3. Bagian Sidebar (Filter Kontrol)
        st.sidebar.header("⚙️ Filter Data")
        
        # Filter Jenis Kelamin
        jk_options = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
        selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
        
        # Filter Tipe Residen
        residen_options = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
        selected_residen = st.sidebar.selectbox("Pilih Tipe Residen:", residen_options)
        
        # Filter Umur (Slider)
        min_age = int(df['Umur'].min())
        max_age = int(df['Umur'].max())
        if min_age == max_age:
            max_age += 1
        selected_age = st.sidebar.slider("Rentang Umur:", min_age, max_age, (min_age, max_age))

        # Terapkan Filter ke Data
        filtered_df = df.copy()
        if selected_jk != "Semua":
            filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == selected_jk]
        if selected_residen != "Semua":
            filtered_df = filtered_df[filtered_df['Tipe Residen'] == selected_residen]
        filtered_df = filtered_df[(filtered_df['Umur'] >= selected_age[0]) & (filtered_df['Umur'] <= selected_age[1])]

        # 4. Header Atas Dashboard
        st.title("📊 Dashboard Analisis Pelanggan")
        st.markdown("Visualisasi data profil pelanggan dan total nilai belanja tahunan secara interaktif.")
        st.markdown("---")

        # 5. Blok Ringkasan Angka Utama (KPI)
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

        # 6. Bagian Grafik Pertama
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("🛒 Total Belanja Berdasarkan Profesi")
            if not filtered_df.empty:
                df_profesi = filtered_df.groupby('Profesi', as_index=False)['Nilai Belanja Setahun'].sum()
                df_profesi = df_profesi.sort_values(by='Nilai Belanja Setahun', ascending=False)
                fig_profesi = px.bar(
                    df_profesi,
                    x='Profesi',
                    y='Nilai Belanja Setahun',
                    text_auto='.2s',
                    color='Profesi',
                    template='plotly_white',
                    labels={'Nilai Belanja Setahun': 'Total Belanja (Rp)'}
                )
                fig_profesi.update_layout(showlegend=False)
                st.plotly_chart(fig_profesi, use_container_width=True)
            else:
                st.info("Tidak ada data yang cocok dengan kriteria filter.")

        with col_chart2:
            st.subheader("🎂 Distribusi Umur Pelanggan")
            if not filtered_df.empty:
                fig_umur = px.histogram(
                    filtered_df,
                    x='Umur',
                    nbins=15,
                    color='Jenis Kelamin',
                    template='plotly_white',
                    labels={'count': 'Jumlah Pelanggan'}
                )
                st.plotly_chart(fig_umur, use_container_width=True)
            else:
                st.info("Tidak ada data yang cocok dengan kriteria filter.")

        st.markdown("---")

        # 7. Bagian Grafik Kedua & Tabel Data Asli
        col_chart3, col_data = st.columns([1, 1.5])

        with col_chart3:
            st.subheader("🏠 Kontribusi Belanja per Tipe Residen")
            if not filtered_df.empty:
                fig_residen = px.pie(
                    filtered_df,
                    names='Tipe Residen',
                    values='Nilai Belanja Setahun',
                    hole=0.4,
                    template='plotly_white'
                )
                fig_residen.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_residen, use_container_width=True)
            else:
                st.info("Tidak ada data yang cocok dengan kriteria filter.")

        with col_data:
            st.subheader("📋 Tabel Ringkasan Data Pelanggan")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

except FileNotFoundError:
    st.error("❌ File **'data_pelanggan (2).csv'** tidak ditemukan! Pastikan file ini diletakkan satu folder dengan file `app.py` kamu.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan sistem saat membaca file: {e}")
