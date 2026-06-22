import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Load Data (dengan Caching agar cepat)
@st.cache_data
def load_data():
    # Menggunakan delimiter ';' sesuai format file kamu
    df = pd.read_csv("data_pelanggan (2).csv", sep=";")
    # Bersihkan nama kolom dari spasi yang tidak diinginkan
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # 3. Sidebar untuk Filter Kontrol
    st.sidebar.header("⚙️ Filter Data")
    
    # Filter Jenis Kelamin
    jk_options = ["Semua"] + list(df['Jenis Kelamin'].unique())
    selected_jk = st.sidebar.selectbox("Pilih Jenis Kelamin:", jk_options)
    
    # Filter Tipe Residen
    residen_options = ["Semua"] + list(df['Tipe Residen'].unique())
    selected_residen = st.sidebar.selectbox("Pilih Tipe Residen:", residen_options)
    
    # Filter Umur (Slider)
    min_age, max_age = int(df['Umur'].min()), int(df['Umur'].max())
    selected_age = st.sidebar.slider("Rentang Umur:", min_age, max_age, (min_age, max_age))

    # Menerapkan Filter ke DataFrame
    filtered_df = df.copy()
    if selected_jk != "Semua":
        filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == selected_jk]
    if selected_residen != "Semua":
        filtered_df = filtered_df[filtered_df['Tipe Residen'] == selected_residen]
    filtered_df = filtered_df[(filtered_df['Umur'] >= selected_age[0]) & (filtered_df['Umur'] <= selected_age[1])]

    # 4. Header Utama Dashboard
    st.title("📊 Customer Analytics Dashboard")
    st.markdown("Dashboard interaktif untuk menganalisis profil dan nilai belanja pelanggan.")
    st.markdown("---")

    # 5. Baris Metrik Utama (KPIs)
    total_pelanggan = len(filtered_df)
    total_belanja = filtered_df['Nilai Belanja Setahun'].sum()
    rata_belanja = filtered_df['Nilai Belanja Setahun'].mean() if total_pelanggan > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👤 Total Pelanggan", value=f"{total_pelanggan} Orang")
    with col2:
        st.metric(label="💰 Total Belanja Setahun", value=f"Rp {total_belanja:,.0f}")
    with col3:
        st.metric(label="📈 Rata-rata Belanja/Pelanggan", value=f"Rp {rata_belanja:,.0f}")

    st.markdown("---")

    # 6. Baris Visualisasi (Grafik)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Distribution Belanja berdasarkan Profesi")
        fig_profesi = px.bar(
            filtered_df.groupby('Profesi', as_index=False)['Nilai Belanja Setahun'].sum().sort_values(by='Nilai Belanja Setahun', ascending=False),
            x='Profesi',
            y='Nilai Belanja Setahun',
            text_auto='.2s',
            color='Profesi',
            template='plotly_white',
            labels={'Nilai Belanja Setahun': 'Total Belanja (Rp)'}
        )
        fig_profesi.update_layout(showlegend=False)
        st.plotly_chart(fig_profesi, use_container_width=True)

    with col_chart2:
        st.subheader("Sebaran Umur Pelanggan")
        fig_umur = px.histogram(
            filtered_df,
            x='Umur',
            nbins=15,
            color='Jenis Kelamin',
            marginal='rug',
            template='plotly_white',
            labels={'count': 'Jumlah Pelanggan'}
        )
        st.plotly_chart(fig_umur, use_container_width=True)

    st.markdown("---")

    # 7. Baris Visualisasi Tambahan (Pie Chart & Ringkasan Data)
    col_chart3, col_data = st.columns([1, 1.5])

    with col_chart3:
        st.subheader("Proporsi Tipe Residen")
        fig_residen = px.pie(
            filtered_df,
            names='Tipe Residen',
            values='Nilai Belanja Setahun',
            hole=0.4,
            template='plotly_white'
        )
        fig_residen.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_residen, use_container_width=True)

    with col_data:
        st.subheader("📋 Data Mentah Terfilter")
        st.dataframe(
            filtered_df[['Customer_ID', 'Nama Pelanggan', 'Jenis Kelamin', 'Umur', 'Profesi', 'Tipe Residen', 'Nilai Belanja Setahun']],
            use_container_width=True,
            hide_index=True
        )

except FileNotFoundError:
    st.error("❌ File 'data_pelanggan (2).csv' tidak ditemukan! Pastikan file CSV berada di folder yang sama dengan file script python ini.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan saat membaca data: {e}")
