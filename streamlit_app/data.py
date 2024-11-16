import streamlit as st
import pandas as pd
import numpy as np

st.cache_data(show_spinner='Fetching data from Database...') # nanti ubah ke postgress
def get_data():
    # buat function untuk data nya
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/1pkqLHjqbjOZq1avSZscC4K6vlhpbD6pBAaui2N7-HT4/pub?gid=0&single=true&output=csv')
    df['Burn Rate'] = df['Burn Rate'].str.replace(',', '.').astype(float) # only for gsheet
    df['Mental Fatigue Score'] = df['Mental Fatigue Score'].str.replace(',', '.').astype(float) # only for gsheet
    return df
