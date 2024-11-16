import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import gspread
import pytz

st.cache_data.clear()


# layout config
st.set_page_config(page_title="Burnout Report", 
                   layout="wide", 
                   page_icon="📊")

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/RiziqAden/GoldenTeam_TSDN2024/refs/heads/main/GoldenSehat.png")
    st.markdown("""
                <h1 style='text-align: center;'>
                    GOLDEN SEHAT
                """,unsafe_allow_html = True)

# to using this you can uncomment this block code and change you key sheet and ghseet api 
# def get_data_to_gsheet(sheetname, data):
#     """
#     Insert a data
#     """
#     gc = gspread.service_account(filename="streamlit_app/key/my_key.json")
#     sh = gc.open_by_key("gsheet_key") # MP real

#     # # select sheet 
#     worksheet_1 = sh.worksheet(f"Sheet1") 
#     # worksheet_1.clear() # clear worksheet 

#     # worksheet_1.update([df.columns.values.tolist()] + df.fillna("").values.tolist()) # < this for update new format
#     worksheet_1.append_rows(data.values.tolist()) # append value when sumbit  


# helper function to get a recomendation
def get_burnout_recommendation(burnout_rate):
    """
    Memberikan rekomendasi berdasarkan tingkat burnout.
    """
    if burnout_rate < 0 or burnout_rate > 1:
        return "Invalid burnout rate. Harap berikan nilai antara 0,0 dan 1,0."
    
    if 0.0 <= burnout_rate <= 0.2:
        return st.success("Low Burnout: Individu tersebut kemungkinan seimbang dan mengelola stres secara efektif. "
                "Dorong kelanjutan praktik saat ini dan check-in kesehatan sesekali.")
    
    elif 0.2 < burnout_rate <= 0.4:
        return st.info("Moderate Burnout: Individu mungkin mengalami stres ringan atau tanda-tanda awal kelelahan. "
                "Rekomendasikan teknik manajemen stres, istirahat teratur, perhatian, dan komunikasi terbuka.")
    
    elif 0.4 < burnout_rate <= 0.6:
        return st.warning("Approaching High Burnout: Ini menunjukkan kelelahan sedang yang mungkin perlu diperhatikan. "
                "Terapkan strategi manajemen stres yang kuat, pertimbangkan penyesuaian beban kerja, dan tawarkan sumber daya seperti konseling.")
    
    elif 0.6 < burnout_rate <= 0.8:
        return st.warning("High Burnout: Individu tersebut kemungkinan mengalami kelelahan yang signifikan. "
                "Tindakan segera dianjurkan, termasuk pengurangan beban kerja, memberikan cuti, dan menawarkan dukungan kesehatan mental.")
    
    elif 0.8 < burnout_rate <= 1.0:
        return st.error("Critical Burnout: Ini adalah tingkat kelelahan kritis yang membutuhkan intervensi mendesak. "
                "Langkah-langkah segera harus mencakup evaluasi medis, cuti yang signifikan, dan dukungan kesehatan mental yang komprehensif.")

# disable when one click
def disable():
    st.session_state.disabled = True

if "disabled" not in st.session_state:
    st.session_state.disabled = False

# load weight model
pipeline = joblib.load('models/pipeline.pkl')
model = joblib.load('models/model_burnout.pkl')

# streamlit page

# this page for to make a data predictions
st.markdown("<h2 style='text-align: center;'>Apakah karyawan Anda kelelahan?</h2>", unsafe_allow_html=True)
st.caption('Jika tombol kirim tidak aktif, Anda dapat menekan Ctrl+Shift+R.')
st.markdown('<br>', unsafe_allow_html=True)

# predictions form
with st.expander("Silakan lengkapi formulir di sini. 👈"):
    with st.form('form_1', border=False):

        # gender
        st.subheader('1. Gender*') # str
        gender = st.radio('Choose the Gender', ['Female', 'Male'], 
                            help = 'Jenis kelamin karyawan.')
        st.markdown('<br>', unsafe_allow_html=True)

        # Company Type
        st.subheader('2. Company Type*') # str
        company_type = st.radio('Choose Company Type', ['Service', 'Product'], 
                                help = 'Jenis perusahaan tempat karyawan bekerja.')
        st.markdown('<br>', unsafe_allow_html=True)
        
        # WFH Setup Available
        st.subheader('3. WFH Setup Available*') # str
        is_wfh = st.radio('Choose WFH Setup Available', ['Yes', 'No'], 
                            help = 'Apakah fasilitas bekerja dari rumah (WFH) tersedia untuk karyawan?')
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Designation
        st.subheader('4. Designation*') # float
        designation = st.radio('Choose Designation', [i for i in range(6)], 
                                help = "Jabatan karyawan dalam organisasi, dinilai pada skala dari 0 hingga 5, dengan angka yang lebih tinggi menunjukkan posisi yang lebih tinggi.",
                                horizontal = True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Resource Allocation
        st.subheader('5. Resource Allocation*') # float
        resource = st.radio('Choose the Resource Allocation', [i+1 for i in range(10)],
                            help = 'Jumlah jam kerja yang diberikan kepada karyawan, mulai dari 1 hingga 10 (di mana angka yang lebih tinggi berarti lebih banyak jam).',
                            horizontal = True)
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Resource Allocation
        st.subheader('6. Mental Fatigue Score*') 
        mental = st.slider('Choose the Mental Fatigue Score', 
                            min_value=0.0, max_value=10.0, value=5.0, step=0.1,
                            help = 'Tingkat kelelahan mental yang dialami karyawan, dinilai pada skala dari 0,0 hingga 10,0, di mana 0,0 menunjukkan tidak ada kelelahan dan 10,0 menunjukkan kelelahan total.')
        st.markdown('<br>', unsafe_allow_html=True)
        

        # completion form button        
        b1 = st.form_submit_button('Submit Here 👈', on_click=disable, disabled=st.session_state.disabled)

# # result of completion form
if b1:
    # # Create input DataFrame
    input_data = {
        'Gender': [gender],
        'Company Type': [company_type],
        'WFH Setup Available': [is_wfh],
        'Designation': [designation],
        'Resource Allocation': [resource],
        'Mental Fatigue Score': [mental],
    }
    # st.dataframe(input_data) # testing
    # layer 
    col1_sb, col2_sb = st.columns([1, 4])

    # predictions
    with st.spinner(text="In progress..."):
        to_frame = pd.DataFrame(input_data)
        input_data = pipeline.transform(to_frame)
        predictions = model.predict(input_data)

        # to ghseet
        to_frame['Burn Rate'] = np.round(predictions[0],2)
        to_frame['Timestamp'] = '{:%Y-%m-%d %H:%M}'.format(datetime.now(tz = pytz.timezone('Asia/Jakarta')))
        get_data_to_gsheet('Sheet1', to_frame)
        with col1_sb:
            st.markdown(f"<h3 style='text-align: center;'>Burnout Rate : {predictions[0] * 100:.2f}%</h3>", unsafe_allow_html=True)
        with col2_sb:
            get_burnout_recommendation(predictions)
else:
    st.info('Silakan isi formulir ini untuk mendapatkan wawasan yang lebih baik')





