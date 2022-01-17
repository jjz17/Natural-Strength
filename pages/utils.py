import os

import pandas as pd
import streamlit as st


def insert_space():
    st.markdown('#')


def insert_horizontal_separator():
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


def lbs_to_kg(lbs: float) -> float:
    return lbs * 0.453592


def kg_to_lbs(kg: float) -> float:
    return kg * 2.20462


@st.cache
def load_model_training_data():
    return pd.read_csv(f'data{os.path.sep}model_training_data.csv')


@st.cache
def load_record_data():
    return pd.read_csv(f'data{os.path.sep}current_usapl_american_raw_records.csv')
