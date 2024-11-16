import streamlit as st
import pandas as pd
import numpy as np

# clear cache
st.cache_data.clear()

# layout config
st.set_page_config(page_title="Burnout Report", 
                   layout="wide", 
                   page_icon="📊")

# st.error("⛔️ development mode⛔️")


st.markdown("<h2 style='text-align: center;'>Employees Burning Out</h2>", unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/RiziqAden/GoldenTeam_TSDN2024/refs/heads/main/GoldenSehat.png")
    st.markdown("""
                <h1 style='text-align: center;'>
                    GOLDEN SEHAT
                """,unsafe_allow_html = True)

    
with st.container(border=True):
    st.markdown("""
                <h6 style='text-align: center;'>
                    Kami membuat aplikasi ini untuk membantu perusahaan menilai kelelahan karyawan dan meningkatkan kesadaran tentang kesehatan mental di antara pengguna kami.
                    <br>
                    *The prediction results may not be accurate.
                    <br><br>
                </h6>

                Ada 2 bagian dalam navigasi: Insights and Predictions.
                <br>
                1. bagian Insights memberikan wawasan tentang bagaimana karyawan dapat mengalami kelelahan.
                <br>
                2. bagian Predictions  menawarkan prediksi tentang seberapa besar kelelahan karyawan berdasarkan fitur.
                <br><br>

                <h6 style='text-align: center;'> 
                    Good Luck 😁 
                </h6>
                """, unsafe_allow_html = True)

