import numpy as np
import pandas as pd
import streamlit as st
from pages import utils as u
import os

# @st.cache
def app():
    @st.cache
    def load_record_data():
        return pd.read_csv(f'data{os.path.sep}current_usapl_american_raw_records.csv')

    # function to generate select box options
    def generate_options(category: str):
        options = np.sort(record_data[category].unique())
        options = list(options)
        options.insert(0, '<select>')
        return options

    def query_args(*queries):
        df = record_data.copy()
        for query in queries:
            if query[1] != '<select>':
                df = df[df[query[0]] == query[1]]
        return df

    record_data = load_record_data()
    numerics = record_data.select_dtypes('number').columns

    dataExploration = st.container()

    with dataExploration:
        # st.write(f'{os.path.abspath(__file__)}')
        st.title('Natural Strength Building')
        st.subheader('Progress With Real Raw Data')
        st.header('Dataset: American USAPL Raw Powerlifting Records')
        st.markdown('Dataset retrieved from: https://usapl.liftingdatabase.com/')
        st.markdown('**It contains the current Male and Female American Raw Powerlifting Records recorded by USAPL**')
        st.text('USAPL athletes are tested and guaranteed to be natural athletes')
        st.write(record_data)

    u.insert_space()

    dataQuerying = st.container()

    with dataQuerying:
        st.subheader('Query the Records')

        weight_col, lift_col, sex_col = st.columns(3)

        with weight_col:
            # Weight Class
            wc_category = 'Weight Class'
            wc_options = generate_options(wc_category)
            wc = st.selectbox(wc_category, wc_options)
            wc_input = (wc_category, wc)
            st.write('You selected:', wc)

        with lift_col:
            # Lift
            lift_category = 'Lift'
            lift_options = generate_options(lift_category)
            lift = st.selectbox(lift_category, lift_options)
            lift_input = (lift_category, lift)
            st.write('You selected:', lift)

        with sex_col:
            # Sex
            sex_category = 'Sex'
            sex_options = generate_options(sex_category)
            sex = st.selectbox(sex_category, sex_options)
            sex_input = (sex_category, sex)
            st.write('You selected:', sex)

        st.write(query_args(wc_input, lift_input, sex_input))
