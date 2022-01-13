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

    def compute_age_class(age: int):
        classes = [15, 17, 19, 23, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 999]

        for _class in classes:
            if age <= _class:
                return _class
        # If not in previous classes, return max age class
        return classes[-1]

    # ['13-15', '16-17', '18-19', '20-23', '24-34', '35-39', '40-44',
    #  '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
    #  '80-999']

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

    weightClass = st.container()

    with weightClass:
        weight_input = st.number_input(
            'Let\'s figure out your weight class', min_value=0, max_value=1500)
        st.write(f'Your weight class is {compute_weight_class(weight_input)} Kg')