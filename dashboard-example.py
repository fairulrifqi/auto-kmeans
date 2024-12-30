import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk load data
def load_data():
    df = pd.read_csv("clean_df_day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['mnth'] = pd.Categorical(df['mnth'], categories=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], ordered=True)
    df['weekday'] = pd.Categorical(df['weekday'], categories=[
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ], ordered=True)
    return df

# Load data
df = load_data()

# Streamlit app
st.title("Dashboard Bike Sharing Dataset")

# Filter Tahun dan Bulan
st.sidebar.header("Filter Data")
selected_years = st.sidebar.multiselect("Pilih Tahun", options=df['yr'].unique(), default=df['yr'].unique())
selected_months = st.sidebar.multiselect("Pilih Bulan", options=df['mnth'].unique(), default=df['mnth'].unique())

# Filter DataFrame
filtered_df = df[(df['yr'].isin(selected_years)) & (df['mnth'].isin(selected_months))]

# 1. Trend Penyewaan Sepeda dalam Dua Tahun Terakhir (Line Chart per Hari)
st.header("1. Trend Penyewaan Sepeda Dua Tahun Terakhir (Harian)")
daily_rentals = filtered_df.groupby('dteday')['cnt'].sum().reset_index()

# Membuat line chart menggunakan plotly express
fig1 = px.line(daily_rentals, x='dteday', y='cnt',
             title="Trend Penyewaan Sepeda Harian",
             labels={'dteday': 'Tanggal', 'cnt': 'Total Penyewaan'}
             )

# Update layout untuk menampilkan bulan di sumbu x
fig1.update_xaxes(
    tickformat="%b",  # Format untuk menampilkan bulan (mis., Jan, Feb, Mar)
    dtick="M1"        # Menampilkan tick setiap bulan
)

st.plotly_chart(fig1)
st.write("Grafik ini menunjukkan tren penyewaan sepeda harian selama dua tahun terakhir.")


# 2. Bulan dengan Penyewaan Terbanyak
st.header("2. Bulan dengan Penyewaan Terbanyak")
monthly_rentals = filtered_df.groupby('mnth')['cnt'].sum().reset_index()

fig2 = px.bar(monthly_rentals, x='mnth', y='cnt',
              title="Total Penyewaan Sepeda Per Bulan",
              labels={'mnth': 'Bulan', 'cnt': 'Total Penyewaan'},
              text='cnt',
              color_discrete_sequence=px.colors.sequential.Viridis)
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2)

# 3. Perbandingan Penyewaan Member dan Non-Member
st.header("3. Perbandingan Penyewaan Member dan Non-Member")
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()

fig3 = px.pie(names=['Non-Member', 'Member'], values=[total_casual, total_registered],
              title="Perbandingan Penyewaan Member dan Non-Member",
              color_discrete_sequence=px.colors.qualitative.Pastel,
              hole=0.3)
st.plotly_chart(fig3)

# 4. Kondisi Penyewaan Berdasarkan Hari
st.header("4. Kondisi Penyewaan Berdasarkan Hari")
daily_rentals = filtered_df.groupby('weekday')['cnt'].mean().reset_index()

fig4 = px.bar(daily_rentals, x='weekday', y='cnt',
              title="Rata-rata Penyewaan Sepeda Per Hari",
              labels={'weekday': 'Hari', 'cnt': 'Rata-rata Penyewaan'},
              color_discrete_sequence=px.colors.sequential.Magma,
              text='cnt')
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4)

# 5. Kondisi Penyewaan per Cuaca (Bar Chart Sederhana)
st.header("5. Kondisi Penyewaan Per Cuaca")
weather_rentals = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()

# Membuat bar chart sederhana menggunakan go.Figure dan go.Bar
fig5 = go.Figure(data=[go.Bar(x=weather_rentals['weathersit'], y=weather_rentals['cnt'])])

# Update layout chart
fig5.update_layout(
    title="Rata-rata Penyewaan Sepeda Per Kondisi Cuaca",
    xaxis_title="Kondisi Cuaca",
    yaxis_title="Rata-rata Penyewaan",
    xaxis=dict(type='category')  # Memaksa sumbu x menjadi kategori
)
st.plotly_chart(fig5)