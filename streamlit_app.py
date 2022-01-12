import numpy as np
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



def query_records(weight_class: float, lift: str = '', sex: str = 'M'):
    if lift == '':
        return record_data[(record_data['Weight Class'] == weight_class) & (record_data['Sex'] == sex)]
    else:
        return record_data[
            (record_data['Weight Class'] == weight_class) & (record_data['Lift'] == lift) & (record_data['Sex'] == sex)]


def query_kwargs(**kwargs):
    # for key, value in kwargs.items():
    #     print("%s == %s" % (key, value))
    df = record_data.copy()
    for category, value in kwargs.items():
        df = df[df[category] == value]
    return df



# Driver code
# myFun(first='Geeks', mid='for', last='Geeks')

# st.write(query_records(52.0))
# st.write(query_records(60.0, 'Raw Open - Bench press single lift'))

# option = st.selectbox(
#     'Weight Class',
#     (52.0, 56.0, 60.0))

weight_classes = np.sort(record_data['Weight Class'].unique())
weight_classes = list(weight_classes)
weight_classes.insert(0, '<select>')
# np.insert(weight_classes, 0, '<select>')
weight_class = st.selectbox('Weight Class', weight_classes)

st.write('You selected:', weight_class)

lift = st.selectbox(
    'Lift',
    np.sort(record_data['Lift'].unique()))

st.write('You selected:', lift)

sex = st.selectbox(
    'Sex',
    np.sort(record_data['Sex'].unique()))

st.write('You selected:', sex)

st.write(query_records(weight_class, lift, sex))
