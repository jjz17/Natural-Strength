import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pages import utils

def app():
    st.subheader('Data Visualizations')

    data = utils.load_model_training_data()

    plt.figure(figsize=(9, 6))
    g = sns.countplot(x='AgeClass', data=data)
    st.pyplot()