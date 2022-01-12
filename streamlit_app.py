import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import streamlit as st

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
numerics = record_data.select_dtypes('number').columns

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

units = st.sidebar.radio('Units', ['Lbs', 'Kg'])
# Toggle global variable
if units == 'Lbs':
    metric_units = False
else:
    metric_units = True

# st.sidebar.write(units)
# st.sidebar.write(metric_units)

weight_input = st.sidebar.number_input(
    'Let\'s figure out your weight class', min_value=0, max_value=1500)
st.sidebar.write(f'Your weight class is {compute_weight_class(weight_input)}')



hist_data = st.sidebar.selectbox('Category', options=numerics)

fig = plt.figure(figsize=(10, 4))
sns.distplot(record_data['Weight (kg)'])
st.pyplot(fig)
