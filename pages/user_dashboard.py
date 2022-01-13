import _pickle as cPickle

import joblib
import numpy as np
import pandas as pd
import streamlit as st


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

    def compute_weight_class(weight: float) -> float:
        if not metric_units:
            weight = lbs_to_kg(weight)
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

    def encode_and_bind(original_dataframe, feature_to_encode):
        dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
        res = pd.concat([original_dataframe, dummies], axis=1)
        res = res.drop([feature_to_encode], axis=1)
        return res

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

    ageClass = st.container()

    with ageClass:
        age_input = st.number_input(
            'Let\'s figure out your age class', min_value=0, max_value=200)
        user_age_class = compute_age_class(age_input)
        st.write(f'Your age class is {user_age_class[0]}-{user_age_class[1]}')

    st.header('Let\'s Set Some Goals!')

    predictBench = st.container()

    with predictBench:
        st.header('Scaled set stats')
        # ['Sex', 'Age', 'AgeClass', 'BodyweightKg', 'WeightClassKg', 'Best3BenchKg', 'Best3SquatKg']
        # Age
        # 17.50
        # BodyweightKg
        # 72.45
        # Best3BenchKg
        # 107.50
        # Best3SquatKg
        # 165.00
        # Sex_F
        # 0.00
        # Sex_M
        # 1.00
        # AgeClass_18 - 19
        # 1.00
        # AgeClass_20 - 23
        # 0.00
        # AgeClass_24 - 34
        # 0.00
        # AgeClass_35 - 39
        # 0.00
        # WeightClassKg_100
        # 0.00
        # WeightClassKg_105
        # 0.00
        # WeightClassKg_110
        # 0.00
        # WeightClassKg_120
        # 0.00
        # WeightClassKg_120 + 0.00
        # WeightClassKg_125
        # 0.00
        # WeightClassKg_125 + 0.00
        # WeightClassKg_40
        # 0.00
        # WeightClassKg_43
        # 0.00
        # WeightClassKg_44
        # 0.00
        # WeightClassKg_47
        # 0.00
        # WeightClassKg_48
        # 0.00
        # WeightClassKg_52
        # 0.00
        # WeightClassKg_53
        # 0.00
        # WeightClassKg_56
        # 0.00
        # WeightClassKg_57
        # 0.00
        # WeightClassKg_59
        # 0.00
        # WeightClassKg_60
        # 0.00
        # WeightClassKg_63
        # 0.00
        # WeightClassKg_66
        # 0.00
        # WeightClassKg_67
        # .5
        # 0.00
        # WeightClassKg_69
        # 0.00
        # WeightClassKg_72
        # 0.00
        # WeightClassKg_74
        # 1.00
        # WeightClassKg_75
        # 0.00
        # WeightClassKg_76
        # 0.00
        # WeightClassKg_82
        # .5
        # 0.00
        # WeightClassKg_83
        # 0.00
        # WeightClassKg_84
        # 0.00
        # WeightClassKg_84 + 0.00
        # WeightClassKg_90
        # 0.00
        # WeightClassKg_90 + 0.00
        # WeightClassKg_93
        # 0.00
        stats = [19, lbs_to_kg(136), lbs_to_kg(195), lbs_to_kg(210), 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        scaler = joblib.load(f'Bench_scaler')
        scaled_stats = scaler.transform(np.array(stats).reshape(1, -1))
        st.write(scaled_stats)
        # scaled_stats2

        ######################
        # Pre-built model
        ######################

        # Reads in saved model
        load_model = cPickle.load(open(f'Bench_model.pickle', 'rb'))

        # Apply model to make predictions
        prediction = load_model.predict(np.array(scaled_stats).reshape(1, -1))
        st.write(f'Predicted bench: {prediction}')

    predictSquat = st.container()

    predictDeadlift = st.container()

# Link to highlight points in a graph
# 'https://www.futurelearn.com/info/courses/data-visualisation-with-python-seaborn-and-scatter-plots/0/steps/193495'
