import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analisis Data", layout="wide")

# Judul aplikasi
title_html = """
    <h1 style="text-align: center;">📊 Dashboard Analisis Data </h1>
    <h3 style="text-align: center;">by: Muhammad Teguh Alfian </h3>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("---")

# Load dataset
def load_data():
    df = pd.read_csv("hour.csv")
    df = df.rename(columns={
        'yr': 'year',
        'mnth': 'month',
        'hum': 'humidity',
        'weathersit': 'weather',
        'cnt': 'count',
        'hr': 'hour',
        'dteday': 'day date',
        'temp': 'temperature'
    })
    df["day date"] = pd.to_datetime(df["day date"])
    
    # Menentukan waktu dalam kategori pagi, siang, sore, malam
    def assign_time_of_day(hour):
        if 6 <= hour < 12:
            return 'Pagi'
        elif 12 <= hour < 16:
            return 'Siang'
        elif 16 <= hour < 20:
            return 'Sore'
        else:
            return 'Malam'
    
    df['waktu'] = df['hour'].apply(assign_time_of_day)
    df['year'] = df['year'].map({0: 2011, 1: 2012})
    df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    df['weather'] = df['weather'].map({1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'})
    return df

df = load_data()

# Menampilkan data
st.subheader("📌 Dataset Bike Sharing")
page_size = 10
page_number = st.number_input("Pilih halaman", min_value=1, max_value=(len(df) // page_size) + 1, step=1)
start_idx = (page_number - 1) * page_size
end_idx = start_idx + page_size
st.write(df.iloc[start_idx:end_idx])
st.markdown("---")

# Statistik Deskriptif
st.subheader("📊 Statistik Dataset")
st.write(df.describe())
st.markdown("---")

# Layout dua kolom
col1, col2 = st.columns(2)

# Visualisasi jumlah Penyewaan Sepeda berdasarkan musim
with col1:
    st.subheader("🌦️ Visualisasi Jumlah Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(data=df, x="season", y="count", ax=ax)
    st.pyplot(fig)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Sepeda Disewa")
    with st.expander("Kesimpulan"):
        st.write("Jumlah pengguna bervariasi berdasarkan musim. Musim tertentu memiliki jumlah pengguna lebih tinggi dibandingkan yang lain.")

# Visualisasi jumlah Penyewaan Sepeda berdasarkan cuaca
with col2:
    st.subheader("🌤️ Visualisasi Jumlah Penyewaan Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(data=df, x="weather", y="count", ax=ax)
    st.pyplot(fig)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Sepeda Disewa")
    with st.expander("Kesimpulan"):
        st.write("Kondisi cuaca mempengaruhi jumlah penyewaan sepeda. Cuaca yang lebih baik cenderung meningkatkan jumlah pengguna. "
        "Penyewaan sepeda paling banyak terdapat pada cuaca cerah dan paling sedikit pada cuaca hujan lebat")

st.markdown("---")

col3, col4 = st.columns(2)

# Visualisasi Pie Chart untuk distribusi Penyewaan Sepeda berdasarkan waktu
with col3:
    st.subheader("🕒 Distribusi Penyewaan Sepeda Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(5, 3.75))
    time_counts = df.groupby("waktu")["count"].sum()
    ax.pie(time_counts, labels=time_counts.index, autopct='%1.1f%%', startangle=90, colors=["#FFD700", "#FFA500", "#FF4500", "#483D8B"])
    ax.axis("equal")
    st.pyplot(fig)
    with st.expander("Kesimpulan"):
        st.write("Penyewaan sepeda lebih tinggi pada waktu tertentu, seperti sore dan pagi hari. Sementara penyewaan sepeda"
        " paling sedikit terjadi pada malam hari ")
with col4:
    st.subheader("📈 Tren Bulanan Penyewaan Sepeda per Tahun")
    fig, ax = plt.subplots(figsize=(5, 4))
    monthly_trend = df.groupby(["year", "month"])["count"].sum().reset_index()
    sns.lineplot(data=monthly_trend, x="month", y="count", hue="year", marker="o", ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Sepeda Disewa")
    st.pyplot(fig)
    with st.expander("Kesimpulan"):
        st.write("Pada tahun 2011, penyewaan meningkat dari Januari hingga Juni, lalu menurun secara bertahap hingga Desember. Lalu, pada tahun 2012,"
        " Penyewaan meningkat dari Januari hingga September, dengan lonjakan tajam dari Februari ke Maret, "
        "lalu menurun dari Oktober hingga Desember. Dilihat dari grafiknya, tren bulanan penyewaan sepeda menunjukkan pola "
        "yang meningkat pada tahun 2012 dibandingkan tahun 2011.")

st.markdown("---")

# Kesimpulan
st.subheader("✅ Kesimpulan")
st.markdown("""
Dari analisis data penyewaan sepeda, diperoleh beberapa kesimpulan utama:

1. **Pengaruh Musim**: Musim sangat berpengaruh terhadap penyewaan sepeda. **Musim gugur** memiliki rata-rata penyewaan tertinggi, sedangkan **musim dingin** memiliki penyewaan terendah.
2. **Pengaruh Cuaca**: Cuaca juga memengaruhi penyewaan sepeda. **Cuaca cerah** meningkatkan penyewaan, sedangkan **hujan atau salju lebat** mengurangi jumlah penyewa.
3. **Hari Kerja vs Akhir Pekan**: Penyewaan sepeda lebih tinggi pada **hari kerja** dibandingkan dengan akhir pekan atau hari libur.
4. **Registered User vs Casual User**: **Pengguna terdaftar** lebih sering menyewa sepeda dibandingkan dengan **pengguna biasa**.
5. **Tren Bulanan**:
   - **Tahun 2011**: Penyewaan meningkat dari Januari hingga Juni, lalu menurun secara bertahap hingga Desember.
   - **Tahun 2012**: Penyewaan meningkat dari Januari hingga September, dengan lonjakan tajam dari Februari ke Maret, lalu menurun dari Oktober hingga Desember.
6. **Pengaruh Waktu**: Penyewaan tertinggi terjadi pada **sore hari**, sedangkan penyewaan terendah terjadi pada **malam hari**.

Secara keseluruhan, faktor musim, cuaca, hari, jenis pengguna, tren bulanan, dan waktu sangat memengaruhi jumlah penyewaan sepeda.
""")

st.caption("Copyright 2025, Muhammad Teguh Alfian")