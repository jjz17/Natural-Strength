import _pickle as cPickle

import joblib
import numpy as np
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

    personalData = st.container()

    with personalData:
        st.title('Natural Strength Building')
        st.subheader('Progress With Real Raw Data')
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

    st.text('Each PR estimation is calculated based on your age, weight, sex, and performance in the'
            'other two lifts')

    predictBench = st.container()

    with predictBench:
        # st.header('Scaled set stats')
        stats = [age_input, weight_input, squat_input, deadlift_input, f_sex, m_sex]
        scaler = joblib.load(f'Bench_scaler')
        scaled_stats = scaler.transform(np.array(stats).reshape(1, -1))
        # st.write(scaled_stats)

        ######################
        # Pre-built model
        ######################

        # Reads in saved model
        load_model = cPickle.load(open(f'Bench_model.pickle', 'rb'))

        # Apply model to make predictions
        prediction = load_model.predict(np.array(scaled_stats).reshape(1, -1))[0]
        if not metric_units:
            prediction = utils.kg_to_lbs(prediction)
        st.write(f'Predicted bench: {round(prediction, 2)} {unit_label}')

    predictSquat = st.container()

    with predictSquat:
        # st.header('Scaled set stats')
        stats = [age_input, weight_input, deadlift_input, bench_input, f_sex, m_sex]
        scaler = joblib.load(f'Squat_scaler')
        scaled_stats = scaler.transform(np.array(stats).reshape(1, -1))
        # st.write(scaled_stats)

        ######################
        # Pre-built model
        ######################

        # Reads in saved model
        load_model = cPickle.load(open(f'Squat_model.pickle', 'rb'))

        # Apply model to make predictions
        prediction = load_model.predict(np.array(scaled_stats).reshape(1, -1))[0]
        if not metric_units:
            prediction = utils.kg_to_lbs(prediction)
        st.write(f'Predicted squat: {round(prediction, 2)} {unit_label}')

    predictDeadlift = st.container()

    with predictDeadlift:
        # st.header('Scaled set stats')
        stats = [age_input, weight_input, squat_input, bench_input, f_sex, m_sex]
        scaler = joblib.load(f'Deadlift_scaler')
        scaled_stats = scaler.transform(np.array(stats).reshape(1, -1))
        # st.write(scaled_stats)

        ######################
        # Pre-built model
        ######################

        # Reads in saved model
        load_model = cPickle.load(open(f'Deadlift_model.pickle', 'rb'))

        # Apply model to make predictions
        prediction = load_model.predict(np.array(scaled_stats).reshape(1, -1))[0]
        if not metric_units:
            prediction = utils.kg_to_lbs(prediction)
        st.write(f'Predicted deadlift: {round(prediction, 2)} {unit_label}')

# Link to highlight points in a graph
# 'https://www.futurelearn.com/info/courses/data-visualisation-with-python-seaborn-and-scatter-plots/0/steps/193495'
