import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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

### Opsi Download Data
@st.cache_data
def convert_df(filtered_df):
    return filtered_df.to_csv().encode('utf-8')
csv = convert_df(filtered_df)
st.download_button(
    label = "Unduh Data",
    data = csv,
    file_name='download_sekarwangi.csv',
    mime='text/csv',
    )

st.dataframe(filtered_df)   #menampilkan hasil filter
