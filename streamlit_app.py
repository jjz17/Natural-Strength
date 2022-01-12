import numpy as np
import pandas as pd
import streamlit as st
import random

dataExploration = st.container()

record_data = pd.read_csv('current_usapl_american_raw_records.csv')

with dataExploration:
    st.title('Natural Strength Building')
    st.subheader('Progress With Real Raw Data')
    st.header('Dataset: American USAPL Raw Powerlifting Records')
    st.markdown('I scraped this dataset from... https://usapl.liftingdatabase.com/')
    st.markdown('**It contains the current Male and Female American Raw Powerlifting Records recorded by USAPL**')
    st.text('Below is the DataFrame')
    st.write(record_data)

# @st.cache
def make_select_box(category: str):
    options = np.sort(record_data[category].unique())
    options = list(options)
    options.insert(0, '<select>')
    return options
    # select_box = st.selectbox(category, options, key=random.random())
    # # user_input = ('Weight Class', weight_class)
    # return select_box


def query_args(*queries):
    df = record_data.copy()
    for query in queries:
        if query[1] != '<select>':
            df = df[df[query[0]] == query[1]]
    return df


wc_category = 'Weight Class'
wc_options = make_select_box(wc_category)
wc = st.selectbox(wc_category, wc_options)
wc_input = (wc_category, wc)

st.write('You selected:', wc)

st.write(query_args(wc_input))
# make_select_box('Lift')

# lift = st.selectbox(
#     'Lift',
#     np.sort(record_data['Lift'].unique()))
#
# st.write('You selected:', lift)
#
# sex = st.selectbox(
#     'Sex',
#     np.sort(record_data['Sex'].unique()))
#
# st.write('You selected:', sex)

# st.write(query_records(weight_class, lift, sex))
query_args(wc_input)