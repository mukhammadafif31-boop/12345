import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Load Data (Kebal Eror & otomatis membersihkan baris kosong)
@st.cache_data
def load_data():
    # Membaca dengan separator ';' dan otomatis melewati baris yang kosong (skip_blank_lines)
    df = pd.read_csv("data_pelanggan (2).csv", sep=";", skip_blank_lines=True)
    
    # Membersihkan baris yang seluruh kolomnya NaN/kosong jika ada
    df = df.dropna(how='all')
    
    # Memastikan spasi di nama kolom dibersihkan
    df.columns = df.columns.str.strip()
    
    # Memastikan tipe data angka benar
    df['Umur'] = pd.to_numeric(df['Umur'], errors='coerce').fillna(0).astype(int)
    df['Nilai Belanja Setahun'] = pd.to_numeric(df['Nilai Belanja Setahun'], errors='coerce').fillna(0).astype(int)
    
    return df

try:
    df = load_data()

    # 3. Sidebar Kontrol Filter
    st.sidebar.header("⚙️ Filter Data")
    
    # Filter Jenis Kelamin
    jk_options = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
    selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
    
    # Filter Tipe Residen
    residen_options = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
    selected_residen = st.sidebar.selectbox("Pilih Tipe Residen:", residen_options)
    
    # Filter Umur (Slider Dinamis)
    min_age = int(df['Umur'].min())
    max_age = int(df['Umur'].max())
    # Jaga-jaga jika min dan max sama agar tidak eror
    if min_age == max_age:
        max_age += 1
    selected_age = st.sidebar.slider("Rentang Umur:", min_age, max_age, (min_age, max_age))

    # Menerapkan Filter ke DataFrame
    filtered_df = df.copy()
    if selected_jk != "Semua":
        filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == selected_jk]
    if selected_residen != "Semua":
        filtered_df = filtered_df[filtered_df['Tipe Residen'] == selected_residen]
    filtered_df = filtered_df[(filtered_df['Umur'] >= selected_age[0]) & (filtered_df['Umur'] <= selected_age[1])]

    # 4. Header Dashboard
    st.title("📊 Dashboard Analisis Pelanggan")
    st.markdown("Dashboard interaktif untuk memantau profil dan performa nilai belanja pelanggan.")
    st.markdown("---")

    # 5. Baris KPI (Ringkasan Angka Utama)
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

    # 6. Baris Visualisasi Grafik Pertama
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
            st.info("Tidak ada data untuk filter ini.")

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
            st.info("Tidak ada data untuk filter ini.")

    st.markdown("---")

    # 7. Baris Visualisasi Kedua & Tabel Data
    col_chart3, col_data = st.columns([1, 1.5])

    with col_chart3:
        st.subheader("🏠 Kontribusi Nilai Belanja per Tipe Residen")
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
            st.info("Tidak ada data untuk filter ini.")

    with col_data:
        st.subheader("📋 Tabel Data Pelanggan Terfilter")
        st.dataframe(
            filtered_df[['Customer_ID', 'Nama Pelanggan', 'Jenis Kelamin', 'Umur', 'Profesi', 'Tipe Residen', 'Nilai Belanja Setahun']],
            use_container_width=True,
            hide_index=True
        )

except FileNotFoundError:
    st.error("❌ File **'data_pelanggan (2).csv'** tidak ditemukan! Pastikan file CSV ditaruh di folder yang sama dengan file `.py` ini.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan: {e}")
