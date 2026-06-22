import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIG
# ==========================
st.set_page_config(
    page_title="Customer Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================
# CSS MODERN
# ==========================
st.markdown("""
<style>
.main{
    background-color:#0E1117;
}
.metric-card{
    background:#1E293B;
    padding:20px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    return pd.read_csv("data_pelanggan.csv", sep=";")

df = load_data()

# ==========================
# SIDEBAR
# ==========================
st.sidebar.title("⚙️ Filter Data")

gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df["Jenis Kelamin"].unique(),
    default=df["Jenis Kelamin"].unique()
)

profesi = st.sidebar.multiselect(
    "Profesi",
    options=df["Profesi"].unique(),
    default=df["Profesi"].unique()
)

filtered_df = df[
    (df["Jenis Kelamin"].isin(gender))
    &
    (df["Profesi"].isin(profesi))
]

# ==========================
# HEADER
# ==========================
st.title("🚀 Customer Analytics Dashboard")
st.markdown("### Analisis Pelanggan dan Nilai Belanja")

# ==========================
# KPI
# ==========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Pelanggan",
        len(filtered_df)
    )

with col2:
    st.metric(
        "💰 Total Belanja",
        f"Rp {filtered_df['Nilai Belanja Setahun'].sum():,.0f}"
    )

with col3:
    st.metric(
        "📈 Rata-rata Belanja",
        f"Rp {filtered_df['Nilai Belanja Setahun'].mean():,.0f}"
    )

with col4:
    st.metric(
        "🎂 Rata-rata Umur",
        round(filtered_df["Umur"].mean(),1)
    )

st.divider()

# ==========================
# CHARTS
# ==========================
c1, c2 = st.columns(2)

with c1:
    fig1 = px.pie(
        filtered_df,
        names="Jenis Kelamin",
        title="Distribusi Gender"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.bar(
        filtered_df.groupby("Profesi")[
            "Nilai Belanja Setahun"
        ].mean().reset_index(),
        x="Profesi",
        y="Nilai Belanja Setahun",
        title="Rata-rata Belanja per Profesi",
        text_auto=True
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================
# ANALISIS UMUR
# ==========================
st.subheader("📊 Distribusi Umur")

fig3 = px.histogram(
    filtered_df,
    x="Umur",
    nbins=10,
    title="Sebaran Umur Pelanggan"
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================
# TOP SPENDER
# ==========================
st.subheader("🏆 Top 10 Pelanggan")

top_customer = (
    filtered_df
    .sort_values(
        "Nilai Belanja Setahun",
        ascending=False
    )
    .head(10)
)

fig4 = px.bar(
    top_customer,
    x="Nama Pelanggan",
    y="Nilai Belanja Setahun",
    color="Profesi",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True)

# ==========================
# SCATTER
# ==========================
st.subheader("🎯 Umur vs Nilai Belanja")

fig5 = px.scatter(
    filtered_df,
    x="Umur",
    y="Nilai Belanja Setahun",
    color="Profesi",
    size="Nilai Belanja Setahun",
    hover_name="Nama Pelanggan"
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================
# DATA TABLE
# ==========================
st.subheader("📋 Data Pelanggan")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==========================
# DOWNLOAD
# ==========================
csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "customer_data.csv",
    "text/csv"
)

# ==========================
# INSIGHT OTOMATIS
# ==========================
st.subheader("🤖 Insight Otomatis")

top_profesi = (
    filtered_df.groupby("Profesi")
    ["Nilai Belanja Setahun"]
    .mean()
    .idxmax()
)

st.success(
    f"Profesi dengan rata-rata belanja tertinggi adalah {top_profesi}"
)

st.info(
    f"Total nilai transaksi mencapai Rp {filtered_df['Nilai Belanja Setahun'].sum():,.0f}"
)