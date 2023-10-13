# -- coding: utf-8 --
"""
Created on Wed Oct  4 11:54:31 2023

@author: Asus
"""

import streamlit as st
import pandas as pd
import openpyxl as opy

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("UMKM Desa Sekarwangi")

st.write("Selamat datang! 👋")

st.write("##### Dashboard ini menyediakan data karakteristik pelaku UMKM di Desa Sekarwangi Kecamatan Soreang.")

import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

chart_data = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=-7.01415,
        longitude=107.5410,
        zoom=14,
        pitch=50,
    )
)
)

st.write("👈 Pilih menu yang diinginkan untuk menampilkan data individu dan agregat UMKM, mengunduh, atau menampilkan data dalam bentuk grafik.")
