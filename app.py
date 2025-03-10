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

st.sidebar.title("🔍 Filter Data")
year_selected = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + list(df["year"].unique()))
weather_selected = st.sidebar.selectbox("Pilih Cuaca", ["Semua Cuaca"] + list(df["weather"].unique()))
season_selected = st.sidebar.selectbox("Pilih Musim", ["Semua Musim"] + list(df["season"].unique()))

if st.sidebar.button("Filter Data"):
    if year_selected != "Semua Tahun":
        df = df[df["year"] == year_selected]
    if weather_selected != "Semua Cuaca":
        df = df[df["weather"] == weather_selected]
    if season_selected != "Semua Musim":
        df = df[df["season"] == season_selected]

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
    st.subheader("🌦️ Visualisasi Rata-Rata (AVG) Jumlah Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(data=df, x="season", y="count", ax=ax)
    st.pyplot(fig)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Sepeda Disewa")
    with st.expander("Penjelasan"):
        st.write("Dari hasil analisis, ternyata perbedaan musim berpengaruh pada penyewaan sepeda. Berikut ini merupakan rata-rata penyewaan dari tertinggi ke terendah:")
        st.write("- **Musim Gugur (Fall):** 236 penyewaan (tertinggi)")
        st.write("- **Musim Panas (Summer):** 208 penyewaan")
        st.write("- **Musim Dingin (Winter):** 198 penyewaan")
        st.write("- **Musim Semi (Spring):** 111 penyewaan (terendah)")
        st.write("\nMusim gugur mencatat jumlah penyewaan sepeda tertinggi dibandingkan musim lainnya, "
        "menunjukkan tingginya minat masyarakat untuk bersepeda saat udara mulai sejuk dan dedaunan berguguran. "
        "Sebaliknya, musim semi memiliki tingkat penyewaan paling rendah, "
        "kemungkinan dipengaruhi oleh cuaca yang masih tidak menentu dan curah hujan yang lebih tinggi.")

# Visualisasi jumlah Penyewaan Sepeda berdasarkan cuaca
with col2:
    st.subheader("🌤️ Visualisasi Rata-Rata (AVG) Jumlah Penyewaan Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(data=df, x="weather", y="count", ax=ax)
    st.pyplot(fig)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Sepeda Disewa")
    with st.expander("Penjelasan"):
        st.write("Cukup jelas dari analisis bahwa cuaca memengaruhi rata-rata jumlah penyewaan sepeda. Berikut ini merupakan rata-rata penyewaan berdasarkan kondisi cuaca:")
        st.write("- **Cerah:** 204 penyewaan (tertinggi)")
        st.write("- **Berkabut:** 175 penyewaan")
        st.write("- **Hujan/Salju Ringan:** 111 penyewaan")
        st.write("- **Hujan/Salju Lebat:** 74 penyewaan (terendah)")
        st.write("\nKita bisa tahu bahwa penyewaan sepeda cenderung meningkat secara signifikan saat cuaca cerah, "
        "ketika kondisi lingkungan lebih mendukung untuk bersepeda dengan nyaman. Sebaliknya, "
        "hujan lebat menjadi faktor utama yang menurunkan jumlah penyewaan, "
        "karena jalanan yang licin dan visibilitas yang terbatas membuat aktivitas bersepeda kurang aman dan nyaman bagi pengguna.")

st.markdown("---")

col3, col4 = st.columns(2)

# Visualisasi Pie Chart untuk distribusi Penyewaan Sepeda berdasarkan waktu
with col3:
    st.subheader("📈 Tren Bulanan (AVG) Penyewaan Sepeda per Tahun")
    fig, ax = plt.subplots(figsize=(5, 4))
    monthly_trend = df.groupby(["year", "month"])["count"].mean().reset_index()
    sns.lineplot(data=monthly_trend, x="month", y="count", hue="year", marker="o", ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-Rata Jumlah Sepeda Disewa")
    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.write("Tren bulanan sewa sepeda merupakan pola perubahan jumlah penyewaan sepeda setiap bulan dalam satu tahun dalam rata-rata. Berikut ini merupakan data di tahun 2011 dan 2012:")
        st.write("**Tahun 2011:** Penyewaan meningkat dari Januari hingga Juni, lalu menurun secara perlahan hingga Desember.")
        st.write("  - Januari 2011: Penyewaan paling sedikit (< 50 sepeda)")
        st.write("  - Juni 2011: Penyewaan tertinggi (~200 sepeda)")
        st.write("**Tahun 2012:** Penyewaan meningkat dari Januari hingga September, lalu menurun hingga Desember.")
        st.write("  - Januari 2012: Penyewaan terendah (< 150 sepeda, lebih baik dari 2011)")
        st.write("  - September 2012: Penyewaan tertinggi (> 300 sepeda)")
        st.write("\nDiketahui bahwa pola penyewaan sepeda menunjukkan tren musiman yang menarik, "
                "di mana jumlah penyewaan cenderung rendah pada awal tahun, "
                "kemungkinan disebabkan oleh cuaca yang kurang mendukung atau rendahnya aktivitas luar ruangan setelah musim liburan. "
                "Seiring berjalannya waktu, angka penyewaan mulai meningkat secara bertahap hingga mencapai puncaknya pada pertengahan tahun, "
                "didorong oleh kondisi cuaca yang lebih stabil serta meningkatnya minat masyarakat untuk beraktivitas di luar ruangan. "
                "Namun, menjelang akhir tahun, jumlah penyewaan kembali menurun, "
                "kemungkinan akibat perubahan cuaca serta meningkatnya kesibukan masyarakat dengan berbagai aktivitas akhir tahun.")
with col4:
    st.subheader("🕒 Distribusi Jumlah (CNT) Penyewaan Sepeda Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(5, 3.75))
    time_counts = df.groupby("waktu")["count"].sum()
    ax.pie(time_counts, labels=time_counts.index, autopct='%1.1f%%', startangle=90, colors=["#FFD700", "#FFA500", "#FF4500", "#483D8B"])
    ax.axis("equal")
    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.write("Apakah waktu juga berpengaruh pada penyewaan sepeda? Jawabannya adalah Ya. Berikut ini merupakan nilai rata-rata penyewaan sepeda berdasarkan empat bagian waktu(Pagi, Siang, Sore, Malam):")
        st.write("- **Sore hari:** 33.4% (tertinggi)")
        st.write("- **Pagi hari:** 27.6%")
        st.write("- **Siang hari:** 22.1%")
        st.write("- **Malam hari:** 16.9% (terendah)")
        st.write("\nPola penyewaan sepeda menunjukkan bahwa aktivitas penyewaan mencapai puncaknya pada sore hari, "
        "saat banyak orang memanfaatkan waktu luang setelah bekerja atau beraktivitas untuk bersepeda, "
        "baik sebagai sarana rekreasi maupun olahraga. Suasana sore yang lebih sejuk dan nyaman "
        "juga menjadi faktor pendukung meningkatnya minat masyarakat dalam bersepeda. "
        "Sebaliknya, jumlah penyewaan sepeda paling sedikit terjadi pada malam hari, "
        "kemungkinan karena keterbatasan pencahayaan, faktor keamanan, "
        "serta menurunnya jumlah orang yang beraktivitas di luar ruangan pada waktu tersebut.")

st.markdown("---")

# Kesimpulan
st.subheader("✅ Kesimpulan")

st.subheader("1. Pengaruh Musim terhadap Penyewaan Sepeda")
st.write("Dari visualisasi di atas, ternyata perbedaan musim berpengaruh pada penyewaan sepeda. Berikut ini merupakan rata-rata penyewaan dari tertinggi ke terendah:")
st.write("- **Musim Gugur (Fall):** 236 penyewaan (tertinggi)")
st.write("- **Musim Panas (Summer):** 208 penyewaan")
st.write("- **Musim Dingin (Winter):** 198 penyewaan")
st.write("- **Musim Semi (Spring):** 111 penyewaan (terendah)")
st.write("\nMusim gugur mencatat jumlah penyewaan sepeda tertinggi dibandingkan musim lainnya, "
"menunjukkan tingginya minat masyarakat untuk bersepeda saat udara mulai sejuk dan dedaunan berguguran. "
"Sebaliknya, musim semi memiliki tingkat penyewaan paling rendah, "
"kemungkinan dipengaruhi oleh cuaca yang masih tidak menentu dan curah hujan yang lebih tinggi..")

st.subheader("2. Pengaruh Cuaca terhadap Penyewaan Sepeda")
st.write("Cukup jelas bahwa cuaca ternyata mempengaruhi rata-rata jumlah penyewaan sepeda. Berikut ini merupakan rata-rata penyewaan berdasarkan kondisi cuaca:")
st.write("- **Cerah:** 204 penyewaan (tertinggi)")
st.write("- **Berkabut:** 175 penyewaan")
st.write("- **Hujan/Salju Ringan:** 111 penyewaan")
st.write("- **Hujan/Salju Lebat:** 74 penyewaan (terendah)")
st.write("\nPenyewaan sepeda cenderung meningkat secara signifikan saat cuaca cerah, "
"ketika kondisi lingkungan lebih mendukung untuk bersepeda dengan nyaman. Sebaliknya, "
"hujan lebat menjadi faktor utama yang menurunkan jumlah penyewaan, "
"karena jalanan yang licin dan visibilitas yang terbatas membuat aktivitas bersepeda kurang aman dan nyaman bagi pengguna.")

st.subheader("3. Di bawah ini merupakan hasil dari analisis Tren Bulanan Rata-Rata Penyewaan Sepeda di 2011 dan 2012: ")
st.write("**Tahun 2011:** Penyewaan meningkat dari Januari hingga Juni, lalu menurun secara perlahan hingga Desember.")
st.write("  - Januari 2011: Penyewaan paling sedikit (< 50 sepeda)")
st.write("  - Juni 2011: Penyewaan tertinggi (~200 sepeda)")
st.write("**Tahun 2012:** Penyewaan meningkat dari Januari hingga September, lalu menurun hingga Desember.")
st.write("  - Januari 2012: Penyewaan terendah (< 150 sepeda, lebih baik dari 2011)")
st.write("  - September 2012: Penyewaan tertinggi (> 300 sepeda)")
st.write("\nDiketahui bahwa pola penyewaan sepeda menunjukkan tren musiman yang menarik, "
"di mana jumlah penyewaan cenderung rendah pada awal tahun, "
"kemungkinan disebabkan oleh cuaca yang kurang mendukung atau rendahnya aktivitas luar ruangan setelah musim liburan. "
"Seiring berjalannya waktu, angka penyewaan mulai meningkat secara bertahap hingga mencapai puncaknya pada pertengahan tahun, "
"didorong oleh kondisi cuaca yang lebih stabil serta meningkatnya minat masyarakat untuk beraktivitas di luar ruangan. "
"Namun, menjelang akhir tahun, jumlah penyewaan kembali menurun, "
"kemungkinan akibat perubahan cuaca serta meningkatnya kesibukan masyarakat dengan berbagai aktivitas akhir tahun.")

st.subheader("4. Pengaruh Waktu terhadap Penyewaan Sepeda")
st.write("Jumlah penyewaan sepeda berdasarkan waktu:")
st.write("- **Sore hari:** 33.4% (tertinggi)")
st.write("- **Pagi hari:** 27.6%")
st.write("- **Siang hari:** 22.1%")
st.write("- **Malam hari:** 16.9% (terendah)")
st.write("\nPola penyewaan sepeda menunjukkan bahwa aktivitas penyewaan mencapai puncaknya pada sore hari, "
"saat banyak orang memanfaatkan waktu luang setelah bekerja atau beraktivitas untuk bersepeda, "
"baik sebagai sarana rekreasi maupun olahraga. Suasana sore yang lebih sejuk dan nyaman "
"juga menjadi faktor pendukung meningkatnya minat masyarakat dalam bersepeda. "
"Sebaliknya, jumlah penyewaan sepeda paling sedikit terjadi pada malam hari, "
"kemungkinan karena keterbatasan pencahayaan, faktor keamanan, serta menurunnya jumlah orang yang beraktivitas di luar ruangan pada waktu tersebut.")

st.subheader(" 🚀Saran Bisnis")
st.write("Berdasarkan kesimpulan di atas, maka kita bisa menerapkan beberapa ide di bawah ini supaya penyewaan sepeda menjadi lebih baik daripada sebelumnya:")
st.write("1. Memberikan diskon khusus pada musim semi dan musim dingin, sehingga orang-orang akan tertarik untuk menyewa sepeda.")
st.write("2. Menyediakan jas hujan untuk orang yang menyewa sepeda.")
st.write("3. Memberikan layanan minuman hangat gratis kepada penyewa saat musim dingin/hujan lebat.")
st.write("4. Menawarkan event khusus yang diadakan pada awal/akhir tahun untuk meningkatkan rata-rata penyewaan sepeda.")
st.write("5. Menambahkan lampu pada sepeda, sehingga pada saat malam hari bisa melihat jalan dengan jelas.")

st.caption("Copyright 2025, Muhammad Teguh Alfian")
