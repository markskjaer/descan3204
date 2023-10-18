import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

### Import Data Lengkap
url = 'https://docs.google.com/spreadsheets/d/1qKf_0z1CcBfFxCejbReILQHVLCV0znxQZc2ob2qjPGg/edit?usp=sharing'
conn  = st.experimental_connection("gsheets", type=GSheetsConnection)
dataumkm = conn.read(spreadsheet=url)
type(dataumkm)
dataumkm["NIK"] = dataumkm["NIK"].astype("string")
dataumkm["No HP"] = dataumkm["No HP"].astype("string")
dataumkm['RW'] = dataumkm['ALAMAT'].str[-5:]
dataumkm['RT'] = dataumkm['ALAMAT'].str[-11:]
df = dataumkm

st.markdown("# Grafik")

#Dropdown Menu
kolom_1 = st.selectbox("Pilih Karakteristik Pertama", dataumkm.columns, index=7)
kolom_2 = st.selectbox("Pilih Karakteristik Kedua", dataumkm.columns, index=17)

###Bar Chart
st.subheader("Grafik Batang")
tes = pd.crosstab(dataumkm[kolom_1],dataumkm[kolom_2])
st.bar_chart(data = tes, height = 700)

st.subheader("Scatter Plot")
st.write("Grafik ini menunjukkan pelaku UMKM di Desa Sekarwangi menurut besarnya modal usaha dan pendapatan usaha per bulan.")
import plotly.express as px
fig = px.scatter(
    data_frame=dataumkm, x="BESARNYA MODAL USAHA", y="PENDAPATAN PER BULAN",color=kolom_1,symbol=kolom_2)
st.plotly_chart(fig)
