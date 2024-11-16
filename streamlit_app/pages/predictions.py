import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys

sys.path.append("streamlit_app")
from data import get_data

# Konfigurasi halaman
st.set_page_config(page_title="Burnout Report", layout="wide", page_icon="📊")

# Sidebar dengan logo dan judul
with st.sidebar:
    st.image("https://raw.githubusercontent.com/RiziqAden/GoldenTeam_TSDN2024/refs/heads/main/GoldenSehat.png")
    st.markdown("""
        <h1 style='text-align: center;'>
            GOLDEN SEHAT
        </h1>
    """, unsafe_allow_html=True)

# Judul utama halaman
st.markdown("<h2 style='text-align: center;'>Employees Burning Out Insight</h2>", unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# Mengambil data
df = get_data()

# Statistik Utama
col1_sb, col2_sb = st.columns([3, 1])

with col1_sb:
    st.markdown(f"<h1 style='text-align: center;'>{'{:,}'.format(df.shape[0])}</h1>", unsafe_allow_html=True)
    st.caption("<h4 style='text-align: center;'>Total of Employees</h4>", unsafe_allow_html=True)

with col2_sb:
    st.markdown(f"<h2 style='text-align: center;'>{df['Timestamp'].max()}</h2>", unsafe_allow_html=True)
    st.caption("<h4 style='text-align: center;'>Data Last Updated</h4>", unsafe_allow_html=True)

# Visualisasi Data
col3_sb, col4_sb = st.columns([2, 3])

with col3_sb:
    gender_distri = px.pie(df, names='Gender', template='plotly_dark', height=450)
    gender_distri.update_layout(title='Distribusi Employees Berdasarkan Jenis Kelamin', legend_title_text='Gender')
    st.plotly_chart(gender_distri, use_container_width=True)

with col4_sb:
    gender_distri_by_product = px.histogram(df, x='Company Type', color='Gender', barmode='group', template='plotly_dark')
    gender_distri_by_product.update_layout(title='Distribusi Jenis Kelamin Berdasarkan Jenis Company', yaxis_title='Gender Count')
    st.plotly_chart(gender_distri_by_product, use_container_width=True)

# Korelasi Mental Fatigue dan Burn Rate
mental_corr_burnrateby_company_type = px.scatter(df, x="Mental Fatigue Score", y="Burn Rate", color="Gender", template='plotly_dark')
mental_corr_burnrateby_company_type.update_layout(title='Correlation of Mental Fatigue Score vs Burn Rate')
st.plotly_chart(mental_corr_burnrateby_company_type, use_container_width=True)

# Tabel Detail
st.markdown("<h6 style='text-align: left;'>Detailed Table of Burned-Out Employees</h6>", unsafe_allow_html=True)
st.dataframe(df.drop('Timestamp', axis=1), use_container_width=True)
