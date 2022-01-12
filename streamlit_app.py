import pandas as pd
import streamlit as st

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


def query_records(weight_class: float, lift: str = ''):
    if lift == '':
        return record_data[record_data['Weight Class'] == weight_class]
    else:
        return record_data[(record_data['Weight Class'] == weight_class) & (record_data['Lift'] == lift)]


st.write(query_records(52.0))
st.write(query_records(60.0, 'Raw Open - Bench press single lift'))
