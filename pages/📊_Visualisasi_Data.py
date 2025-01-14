import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

### Import Data Lengkap
url = 'https://docs.google.com/spreadsheets/d/1qKf_0z1CcBfFxCejbReILQHVLCV0znxQZc2ob2qjPGg/edit?usp=sharing'
conn  = st.connection("gsheets", type=GSheetsConnection)
dataumkm = conn.read(spreadsheet=url)
type(dataumkm)
dataumkm["NIK"] = dataumkm["NIK"].astype("string")
dataumkm["No HP"] = dataumkm["No HP"].astype("string")
dataumkm['ALAMAT'] = dataumkm['ALAMAT'].str.rstrip()
dataumkm['RW'] = dataumkm['ALAMAT'].str[-5:]
dataumkm['RT'] = dataumkm['ALAMAT'].str[-11:]
df = dataumkm

### Filter Data
from pandas.api.types import(
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
    )

st.subheader("Data Lengkap UMKM Desa Sekarwangi")
st.write("Pilih kolom yang ingin ditampilkan")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan UI di atas dataframe untuk memungkinkan pengguna melakukan filter kolom

    Args:
        df(pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe

    Sumber: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
    """
    modify = st.checkbox("Tambahkan filter")
    if not modify:
        return df
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter data berdasarkan", dataumkm.columns)
        for column in to_filter_columns:
            left, right = st.columns((1,20))
            left.write("↳")
            #Treat columns with < 10 unique values a s categorical
            if is_numeric_dtype(df[column]):
                st.write(f'Values for {column}')
                _min = st.text_input('Rentang Terkecil', float(df[column].min()))
                _max = st.text_input('Rentang Tertinggi', float(df[column].max()))
                _min = float(_min)
                _max = float(_max)
                df= df[df[column].between(_min,_max)]
            else:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                    )
                df = df[df[column].isin(user_cat_input)]
        return df
filtered_df = filter_dataframe(df)
df = pd.DataFrame(filtered_df)

st.markdown("# Grafik")

a = st.sidebar.radio('Jumlah Karakteristik yang Ingin Divisualisasikan:', [1, 2])

if a==1:
    #Dropdown Menu
    kolom_1 = st.selectbox("Pilih Karakteristik", dataumkm.columns, index=7)

    ###Bar Chart
    st.subheader("Grafik Batang")
    tes = dataumkm.pivot_table(index=dataumkm[kolom_1],values='NIK',aggfunc='count')
    st.bar_chart(data = tes, height = 700)

    st.subheader("Scatter Plot")
    st.write("Grafik ini menunjukkan pelaku UMKM di Desa Sekarwangi menurut besarnya modal usaha dan pendapatan usaha per bulan.")

    fig = px.scatter(
        data_frame=dataumkm, x="BESARNYA MODAL USAHA", y="PENDAPATAN PER BULAN",color=kolom_1,symbol=kolom_1)
    st.plotly_chart(fig)

elif a==2:
    #Dropdown Menu
    kolom_1 = st.selectbox("Pilih Karakteristik Pertama", dataumkm.columns, index=7)
    kolom_2 = st.selectbox("Pilih Karakteristik Kedua", dataumkm.columns, index=17)

    ###Bar Chart
    st.subheader("Grafik Batang")
    tes = pd.crosstab(dataumkm[kolom_1],dataumkm[kolom_2])
    st.bar_chart(data = tes, height = 700)

    st.subheader("Scatter Plot")
    st.write("Grafik ini menunjukkan pelaku UMKM di Desa Sekarwangi menurut besarnya modal usaha dan pendapatan usaha per bulan.")

    fig = px.scatter(
        data_frame=dataumkm, x="BESARNYA MODAL USAHA", y="PENDAPATAN PER BULAN",color=kolom_1,symbol=kolom_2)
    st.plotly_chart(fig)
