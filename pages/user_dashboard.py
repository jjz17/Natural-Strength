import _pickle as cPickle
import os

import joblib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from pages import utils


# @st.cache
def app():
    # '''
    # GLOBAL VARIABLES
    # '''
    # Units
    metric_units = False
    unit_label = 'Lbs'
    # Sex
    male = True
    m_sex = 1
    f_sex = 0

    def compute_weight_class(weight: float) -> float:
        if not metric_units:
            weight = utils.lbs_to_kg(weight)
        if male:
            weight_classes = [52.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 100.0, 110.0, 125.0, 140.0, 141.0]
        else:
            weight_classes = [44.0, 48.0, 52.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 100.0, 101.0]

        for _class in weight_classes:
            if weight <= _class:
                return _class
        # If not in previous classes, return max weight class
        return weight_classes[-1]

    def compute_age_class(age: int) -> (int, int):
        age_classes = [15, 17, 19, 23, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 999]

        for i, _class in enumerate(age_classes):
            if age <= _class and i >= 1:
                return age_classes[i - 1] + 1, _class
            if age <= _class and i == 0:
                return 13, _class
        # If not in previous classes, return max age class
        return age_classes[-2] + 1, age_classes[-1]

    # ['13-15', '16-17', '18-19', '20-23', '24-34', '35-39', '40-44',
    #  '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
    #  '80-999']

    @st.cache(allow_output_mutation=True)
    def load_model(model_file: str):
        return cPickle.load(open(model_file, 'rb'))

    def scale_stats(scaler, stats: list):
        return scaler.transform(np.array(stats).reshape(1, -1))

    @st.cache
    def load_data():
        return pd.read_csv(f'data{os.path.sep}model_training_data.csv')

    personalData = st.container()

    with personalData:
        # st.title('Natural Strength Building')
        # st.subheader('Progress With Real Raw Data')
        st.header('Your Personal Metrics')
        st.markdown('**Enter your information**')
        # st.text('Below is the DataFrame')

    userInfo = st.container()

    with userInfo:
        units_col, sex_col, weight_col, age_col = st.columns(4)

        with units_col:

            units = st.radio('Units', ['Lbs', 'Kg'])
            unit_label = units
            # Toggle global variable
            if units == 'Lbs':
                metric_units = False
            else:
                metric_units = True
            st.write(f'{units} selected')

        with sex_col:

            user_sex = st.radio('Sex', ['M', 'F'])
            # Toggle global variable
            if user_sex == 'F':
                male = False
                m_sex = 0
                f_sex = 1
            else:
                male = True
                m_sex = 1
                f_sex = 0
            st.write(f'{user_sex} selected')

        with weight_col:

            weight_input = st.number_input(
                'Compute your weight class', min_value=0., max_value=1500.)
            st.write(f'Weight class: {compute_weight_class(weight_input)} Kg')

        with age_col:

            age_input = st.number_input(
                'Compute your age class', min_value=0, max_value=200)
            user_age_class = compute_age_class(age_input)
            st.write(f'Age class: {user_age_class[0]}-{user_age_class[1]}')

    st.header('Let\'s Set Some Goals')
    st.text('Note: the estimation tools are most accurate for ages 18 through 40')

    userLifts = st.container()

    with userLifts:

        bench_col, squat_col, deadlift_col = st.columns(3)

        with bench_col:
            bench_input = st.number_input('Enter your bench', min_value=0., max_value=2000.)
            st.write(f'Your bench is {bench_input} {unit_label}')

        with squat_col:
            squat_input = st.number_input('Enter your squat', min_value=0., max_value=2000.)
            st.write(f'Your squat is {squat_input} {unit_label}')

        with deadlift_col:
            deadlift_input = st.number_input('Enter your deadlift', min_value=0., max_value=2000.)
            st.write(f'Your deadlift is {deadlift_input} {unit_label}')

    # Convert units if necessary
    if not metric_units:
        weight_input = utils.lbs_to_kg(weight_input)
        bench_input = utils.lbs_to_kg(bench_input)
        squat_input = utils.lbs_to_kg(squat_input)
        deadlift_input = utils.lbs_to_kg(deadlift_input)

    utils.insert_space()
    st.text('Estimations based on age, weight, sex, and performance in other two lifts')

    # Load in the models and scalers
    bench_model = load_model(f'models{os.path.sep}bench_model.pickle')
    bench_scaler = joblib.load(f'models{os.path.sep}bench_scaler')
    squat_model = load_model(f'models{os.path.sep}squat_model.pickle')
    squat_scaler = joblib.load(f'models{os.path.sep}squat_scaler')
    deadlift_model = load_model(f'models{os.path.sep}deadlift_model.pickle')
    deadlift_scaler = joblib.load(f'models{os.path.sep}deadlift_scaler')

    maxPredictions = st.container()

    with maxPredictions:
        bench, squat, deadlift = st.columns(3)
        with bench:
            bench_stats = [age_input, weight_input, squat_input, deadlift_input, f_sex, m_sex]
            bench_stats_scaled = scale_stats(bench_scaler, bench_stats)

            bench_pred = bench_model.predict(np.array(bench_stats_scaled).reshape(1, -1))[0]
            if not metric_units:
                bench_pred = utils.kg_to_lbs(bench_pred)
            st.write(f'Predicted bench max: {round(bench_pred, 2)} {unit_label}')

        with squat:
            squat_stats = [age_input, weight_input, bench_input, deadlift_input, f_sex, m_sex]
            squat_stats_scaled = scale_stats(squat_scaler, squat_stats)

            squat_pred = squat_model.predict(np.array(squat_stats_scaled).reshape(1, -1))[0]
            if not metric_units:
                squat_pred = utils.kg_to_lbs(squat_pred)
            st.write(f'Predicted squat max: {round(squat_pred, 2)} {unit_label}')

        with deadlift:
            deadlift_stats = [age_input, weight_input, bench_input, squat_input, f_sex, m_sex]
            deadlift_stats_scaled = scale_stats(deadlift_scaler, deadlift_stats)

            deadlift_pred = deadlift_model.predict(np.array(deadlift_stats_scaled).reshape(1, -1))[0]
            if not metric_units:
                deadlift_pred = utils.kg_to_lbs(deadlift_pred)
            st.write(f'Predicted deadlift max: {round(deadlift_pred, 2)} {unit_label}')

    utils.insert_space()
    st.write('Model Training Data')
    data = load_data()
    st.write(data)

    plot1, plot2 = st.columns(2)

    # plt.figure(figsize=(15, 8))
    # sns.countplot(x='type1', data=pokemon_df, hue='is_legendary')





    # with plot1:
    #     fig = sns.displot(data=data, x='Age', y='TotalKg').figure
    #     st.pyplot(fig)
    # with plot2:
    #     st.subheader('Relationship between Age and Total Kg lifted')
    #     # fig2 = sns.histplot(data=data['TotalKg']).figure
    #     # st.pyplot(fig2)
    #
    # fig3 = sns.relplot(data=data, x='Age', y='TotalKg', hue='Sex', col='Sex')
    # st.pyplot(fig3)





    # st.header('Visualising relationship between numeric variables')
    # st.subheader('Pairplot analysis')
    # g = sns.pairplot(data, vars=["Age", "TotalKg", "BodyweightKg"], dropna=True,
    #                  hue='Sex', diag_kind="kde")
    # g.map_lower(sns.regplot)
    # st.pyplot(g)

# Link to highlight points in a graph
# 'https://www.futurelearn.com/info/courses/data-visualisation-with-python-seaborn-and-scatter-plots/0/steps/193495'
