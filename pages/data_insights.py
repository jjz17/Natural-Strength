import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from pages import utils


def app():
    st.subheader('Data Visualizations')

    data = utils.load_model_training_data()

    plt.figure(figsize=(9, 6))
    fig = sns.countplot(x='AgeClass', data=data).figure
    st.pyplot(fig)

    st.text('Informational figure')
