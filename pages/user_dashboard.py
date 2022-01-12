import streamlit as st
import numpy as np
import pandas as pd


# @st.cache
def app():
    # '''
    # GLOBAL VARIABLES
    # '''
    # Units
    metric_units = False

    # Sex
    male = True

    def lbs_to_kg(lbs):
        return lbs * 0.453592

    def kg_to_lbs(kg):
        return kg * 2.20462

    def compute_weight_class(weight: float):
        if not metric_units:
            weight = lbs_to_kg(weight)
        if male:
            classes = [52.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 100.0, 110.0, 125.0, 140.0, 141.0]
        else:
            classes = [44.0, 48.0, 52.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 100.0, 101.0]

        for _class in classes:
            if weight <= _class:
                return _class
        # If not in previous classes, return max weight class
        return classes[-1]

    personalData = st.container()

    with personalData:
        st.title('Natural Strength Building')
        st.subheader('Progress With Real Raw Data')
        st.header('Your Personal Metrics')
        st.markdown('**Enter your information**')
        # st.text('Below is the DataFrame')

    units = st.radio('Units', ['Lbs', 'Kg'])
    # Toggle global variable
    if units == 'Lbs':
        metric_units = False
    else:
        metric_units = True

    user_sex = st.radio('Sex', ['M', 'F'])
    # Toggle global variable
    if user_sex == 'F':
        male = False
    else:
        male = True

    # st.sidebar.write(units)
    # st.sidebar.write(metric_units)

    weight_input = st.number_input(
        'Let\'s figure out your weight class', min_value=0, max_value=1500)
    st.write(f'Your weight class is {compute_weight_class(weight_input)}')