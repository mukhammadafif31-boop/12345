import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Premium Customer Business Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bersihkan cache agar data selalu segar
st.cache_data.clear()

# 2. Header Atas Dashboard Eksekutif
st.title("💎 Premium Customer Business Intelligence Dashboard")
st.markdown("Analisis visual dan statistik mendalam berbasis data pelanggan secara instan dan interaktif.")
st.markdown("---")

# 3. DATA UTUH DI-EMBED LANGSUNG KE CODINGAN
@st.cache_data
def load_data_langsung():
    raw_data = {
        "Customer_ID": [
            "CUST-001", "CUST-002", "CUST-003", "CUST-004", "CUST-005", 
            "CUST-006", "CUST-007", "CUST-008", "CUST-009", "CUST-010",
            "CUST-011", "CUST-012", "CUST-013", "CUST-014", "CUST-015", 
            "CUST-016", "CUST-017", "CUST-018", "CUST-019", "CUST-020",
            "CUST-021", "CUST-022", "CUST-023", "CUST-024", "CUST-025", 
            "CUST-026", "CUST-027", "CUST-028", "CUST-029", "CUST-030",
            "CUST-031", "CUST-032", "CUST-033", "CUST-034", "CUST-035", 
            "CUST-036", "CUST-037", "CUST-038", "CUST-039", "CUST-040",
            "CUST-041", "CUST-042", "CUST-043", "CUST-044", "CUST-045", 
            "CUST-046", "CUST-047", "CUST-048", "CUST-049", "CUST-050"
        ],
        "Nama Pelanggan": [
            "Budi Anggara", "Shirley Ratuwati", "Agus Cahyono", "Antonius Winarta", "Sri Wahyuni, IR",
            "Rosalina Kurnia", "Cahyono, Agus", "Danang Santosa", "Elisabeth Suryadinata", "Mario Setiawan",
            "Maria Suryawan", "Erliana Widjaja", "Cahaya Putri", "Mario Setiawan", "Suryadi, Agus",
            "Siti Handayani", "Hendry, Kevin", "Rina Susanti", "Andreas, David", "Yulia Lestari",
            "Michael Tan", "Jessica Wijaya", "Stephanus, Andi", "Novianti, Dian", "Roni Gunawan",
            "Yuniar, Linda", "Grace Mulyati", "Adeline Huang", "Tia Hartanti", "Rosita Saragih",
            "Eviana Handry", "Chintya Winarni", "Cecilia Kusnadi", "Deasy Arisandi", "Ida Ayu",
            "Ni Made Suasti", "Felicia Tandiono", "Agatha Chelsea", "Devi Permata", "Indah Lestari",
            "Denny Setiawan", "Hendra Wijaya", "Rudi Hartono", "Santi Rahayu", "Bambang Pamungkas",
            "Dewi Sartika", "Anwar Sadat", "Fatimah Zahra", "Ahmad Fauzi", "Siti Aminah"
        ],
        "Jenis Kelamin": [
            "Pria", "Wanita", "Pria", "Pria", "Wanita",
            "Wanita", "Pria", "Pria", "Wanita", "Pria",
            "Wanita", "Wanita", "Wanita", "Pria", "Pria",
            "Wanita", "Pria", "Wanita", "Pria", "Wanita",
            "Pria", "Wanita", "Pria", "Wanita", "Pria",
            "Wanita", "Wanita", "Wanita", "Wanita", "Wanita",
            "Wanita", "Wanita", "Wanita", "Wanita", "Wanita",
            "Wanita", "Wanita", "Wanita", "Wanita", "Wanita",
            "Pria", "Pria", "Pria", "Wanita", "Pria",
            "Wanita", "Pria", "Wanita", "Pria", "Wanita"
        ],
        "Umur": [
            58, 14, 48, 53, 41, 24, 64, 52, 29, 33,
            50, 49, 64, 60, 36, 42, 28, 31, 45, 22,
            37, 26, 51, 34, 43, 38, 35, 40, 56, 46,
            19, 47, 19, 21, 39, 30, 25, 23, 32, 27,
            44, 35, 50, 29, 55, 33, 48, 24, 31, 41
        ],
        "Profesi": [
            "Wiraswasta", "Pelajar", "Professional", "Professional", "Wiraswasta",
            "Professional", "Wiraswasta", "Professional", "Professional", "Professional",
            "Professional", "Professional", "Wiraswasta", "Wiraswasta", "Wiraswasta",
            "Ibu Rumah Tangga", "Professional", "Professional", "Wiraswasta", "Mahasiswa",
            "Professional", "Professional", "Wiraswasta", "Professional", "Wiraswasta",
            "Professional", "Wiraswasta", "Ibu Rumah Tangga", "Professional", "Ibu Rumah Tangga",
            "Mahasiswa", "Wiraswasta", "Mahasiswa", "Wiraswasta", "Professional",
            "Wiraswasta", "Professional", "Professional", "Wiraswasta", "Professional",
            "Professional", "Wiraswasta", "Professional", "Professional", "Wiraswasta",
            "Professional", "Wiraswasta", "Mahasiswa", "Professional", "Ibu Rumah Tangga"
        ],
        "Tipe Residen": [
            "Sector", "Cluster", "Cluster", "Cluster", "Cluster",
            "Cluster", "Sector", "Cluster", "Sector", "Cluster",
            "Sector", "Sector", "Cluster", "Cluster", "Sector",
            "Cluster", "Cluster", "Sector", "Sector", "Cluster",
            "Cluster", "Sector", "Cluster", "Cluster", "Sector",
            "Sector", "Cluster", "Cluster", "Cluster", "Sector",
            "Cluster", "Sector", "Cluster", "Sector", "Sector",
            "Cluster", "Sector", "Cluster", "Sector", "Cluster",
            "Sector", "Cluster", "Sector", "Cluster", "Sector",
            "Cluster", "Sector", "Cluster", "Sector", "Cluster"
        ],
        "Nilai Belanja Setahun": [
            9497927, 2722700, 5286429, 5204498, 10615206,
            5215541, 9837260, 5223569, 5993218, 5257448,
            5987367, 5941914, 9333168, 9471615, 8912443,
            6215332, 5412990, 5821004, 9112445, 3124550,
            5641223, 5891224, 9314552, 5741229, 9412550,
            5812440, 9114159, 6631680, 5271845, 5020976,
            3042773, 10663179, 3047926, 9759822, 5962575,
            9678994, 5972787, 5634120, 9124550, 5891220,
            5741330, 9214550, 5612440, 5824110, 9812440,
            5712440, 9412330, 3145220, 5812440, 6412550
        ]
    }
    return pd.DataFrame(raw_data)

# Memuat data terintegrasi penuh
df = load_data_langsung()

st.success(f"📊 Dashboard Aktif: {len(df)} Data Pelanggan Terkunci dalam Sistem.")

kolom_angka = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
kolom_teks = df.select_dtypes(include=['object', 'category']).columns.tolist()

# 4. Pengaturan Menu Kontrol di Sidebar
st.sidebar.header("⚙️ Menu Kontrol & Filter")
filtered_df = df.copy()

# Filter Jenis Kelamin
if 'Jenis Kelamin' in df.columns:
    opsi_jk = ["Semua"] + sorted(list(df['Jenis Kelamin'].dropna().unique()))
    pilihan_jk = st.sidebar.selectbox("Filter Jenis Kelamin:", opsi_jk)
    if pilihan_jk != "Semua":
        filtered_df = filtered_df[filtered_df['Jenis Kelamin'] == pilihan_jk]
        
# Filter Tipe Residen
if 'Tipe Residen' in df.columns:
    opsi_residen = ["Semua"] + sorted(list(df['Tipe Residen'].dropna().unique()))
    pilihan_residen = st.sidebar.selectbox("Filter Tipe Residen:", opsi_residen)
    if pilihan_residen != "Semua":
        filtered_df = filtered_df[filtered_df['Tipe Residen'] == pilihan_residen]

# Fitur Pencarian Nama
st.sidebar.markdown("### 📝 Pencarian")
search_query = st.sidebar.text_input("Cari Nama Pelanggan:")
if search_query:
    filtered_df = filtered_df[filtered_df['Nama Pelanggan'].str.contains(search_query, case=False, na=False)]

# 5. Blok Metrik Utama (KPI Korporat)
st.markdown("### 📈 Ringkasan Eksekutif")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📊 Total Pelanggan", value=f"{len(filtered_df)} Orang")
with col2:
    total_nilai = filtered_df['Nilai Belanja Setahun'].sum()
    st.metric(label="💰 Total Belanja", value=f"Rp {total_nilai:,.0f}")
with col3:
    rata_nilai = filtered_df['Nilai Belanja Setahun'].mean() if len(filtered_df) > 0 else 0
    st.metric(label="📈 Rata-rata Belanja", value=f"Rp {rata_nilai:,.0f}")
with col4:
    maks_nilai = filtered_df['Nilai Belanja Setahun'].max() if len(filtered_df) > 0 else 0
    st.metric(label="🏆 Belanja Tertinggi", value=f"Rp {maks_nilai:,.0f}")

st.markdown("---")

# 6. Tata Letak Menggunakan Tab Streamlit
tab1, tab2, tab3 = st.tabs([
    "📊 Visualisasi Grafik", 
    "🔬 Analisis Statistik Deskriptif", 
    "📋 Inspeksi Data & Ekspor"
])

with tab1:
    st.subheader("🛠️ Konfigurasi Grafik")
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        sb_x = st.selectbox("Sumbu X (Kategori):", kolom_teks, index=kolom_teks.index('Profesi'))
    with col_sel2:
        sb_y = st.selectbox("Sumbu Y (Nilai Angka):", kolom_angka, index=kolom_angka.index('Nilai Belanja Setahun'))
        
    st.markdown("---")
    
    if not filtered_df.empty:
        chart_data = filtered_df.groupby(sb_x)[sb_y].sum()
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown(f"#### 📊 Grafik Batang Total {sb_y}")
            st.bar_chart(chart_data)
        with col_chart2:
            st.markdown(f"#### 📈 Grafik Area Tren {sb_y}")
            st.area_chart(chart_data)
    else:
        st.info("Tidak ada data untuk filter ini.")

with tab2:
    st.subheader("🔬 Analisis Ringkasan Matematika & Statistik")
