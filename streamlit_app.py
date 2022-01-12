import numpy as np
import pandas as pd
import streamlit as st


def lbs_to_kg(lbs):
    return lbs * 0.453592


def kg_to_lbs(kg):
    return kg * 2.20462

@st.cache
def load_record_data():
    return pd.read_csv('current_usapl_american_raw_records.csv')


def generate_options(category: str):
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


dataExploration = st.container()

record_data = load_record_data()

with dataExploration:
    st.title('Natural Strength Building')
    st.subheader('Progress With Real Raw Data')
    st.header('Dataset: American USAPL Raw Powerlifting Records')
    st.markdown('I scraped this dataset from... https://usapl.liftingdatabase.com/')
    st.markdown('**It contains the current Male and Female American Raw Powerlifting Records recorded by USAPL**')
    st.text('Below is the DataFrame')
    st.write(record_data)

st.markdown('#')
st.markdown('#')

dataQuerying = st.container()

with dataQuerying:
    st.subheader('Query the Records')
    # st.header('Dataset: American USAPL Raw Powerlifting Records')
    # st.markdown('I scraped this dataset from... https://usapl.liftingdatabase.com/')
    # st.markdown('**It contains the current Male and Female American Raw Powerlifting Records recorded by USAPL**')
    # st.text('Below is the DataFrame')
    # st.write(record_data)

    # Weight Class
    wc_category = 'Weight Class'
    wc_options = generate_options(wc_category)
    wc = st.selectbox(wc_category, wc_options)
    wc_input = (wc_category, wc)
    st.write('You selected:', wc)

    # Lift
    lift_category = 'Lift'
    lift_options = generate_options(lift_category)
    lift = st.selectbox(lift_category, lift_options)
    lift_input = (lift_category, lift)
    st.write('You selected:', lift)

    # Sex
    sex_category = 'Sex'
    sex_options = generate_options(sex_category)
    sex = st.selectbox(sex_category, sex_options)
    sex_input = (sex_category, sex)
    st.write('You selected:', sex)

    st.write(query_args(wc_input, lift_input, sex_input))

side_bar = st.sidebar.selectbox(
    'What is my weight class?',
    ('', "Home phone", "Mobile phone")
)

# # adding a text input widget to the sidebar
#
# add_textbox = st.sidebar.text_input('Enter your name: ')

