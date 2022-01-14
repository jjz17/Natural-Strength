import streamlit as st


def insert_space():
    st.markdown('#')


def lbs_to_kg(lbs: float) -> float:
    return lbs * 0.453592


def kg_to_lbs(kg: float) -> float:
    return kg * 2.20462
