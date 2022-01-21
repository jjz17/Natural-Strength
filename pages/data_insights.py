import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pages import utils

def app():
    st.subheader('Data Visualizations')
    plt.figure(figsize=(9, 6))
    sns.countplot(x='AgeClass', data=data)