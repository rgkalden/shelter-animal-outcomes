import pandas as pd
import plotly.express as px
import streamlit as st
from joblib import load

from functions import *

st.title("ML Predictions")

with st.expander('About this Section'):
    st.write('''
    
    In this section, machine learning is used to predict what the outcome
    will be for animals that arrive at the shelter. Predictions can be used to help
    the shelter devote their efforts to animals who need more help finding a new home
    and being adopted. For example, if an incoming animal is predicted to be transferred to
    another shelter, rather than being adopted, then the shelter would know that is should
    direct more of its efforts to finding a home for that particular animal, compared to an 
    animal that is predicted to be adopted.
    
    
    There are two applications of machine learning that can be viewed in the tabs below:

    - Single Animal Prediction: A form can be filled out with information for a single
      animal, and then a prediction for the outcome will be made.
    - Batch Prediction: For illustration purposes, predictions are made on a sample 
      batch of animals. Descriptive analytics for the overall outcomes are displayed.

    In addition, further information is provided for machine learning model interpretability:
    - Model Interpretation: In order to help interpret the outcomes of the model, the
      relative importance of each feature when making a prediction with the model is 
      displayed in a chart. 
    
    ''')



tab1, tab2, tab3 = st.tabs([ 'Single Animal Prediction', 'Batch Prediction', 'Model Interpretation'])

with tab1:

    with st.form('ml_feat_values'):
        col1, col2 = st.columns(2)
        with col1:
            # AnimalType_Dog

            animal_type = st.selectbox('Animal Type', ('Dog', 'Cat'), index=1)
            if animal_type == 'Dog':
                AnimalType_Dog = 1
            else:
                AnimalType_Dog = 0

        with col2:
            # sex_male

            sex_type = st.selectbox('Animal Sex', ('Male', 'Female'), index=1)
            if sex_type == 'Male':
                sex_male = 1
            else:
                sex_male = 0

        col3, col4 = st.columns(2)
        with col3:
            # age_years

            age_years = st.number_input('Age (years)', max_value=100., min_value=0., value=0.5, step=0.5)

        with col4:
            # month

            month = st.number_input('Month when outcome will occur (1-12)', min_value=1, max_value=12, step=1, value=8)


        col5, col6, col7 = st.columns(3)
        with col5:
        # breed_mix

            breed_bool = st.checkbox('Mixed Breed', value=True)
            if breed_bool:
                breed_mix = 1
            else:
                breed_mix = 0

        with col6:
        # color_single

            color_bool = st.checkbox('Single Color', value=False)
            if color_bool:
                color_single = 1
            else:
                color_single = 0

        with col7:
            # neutered_neutered

            neutered_bool = st.checkbox('Neutered', value=True)
            if neutered_bool:
                neutered_neutered = 1
            else:
                neutered_neutered = 0

        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button:

        feature_values = [age_years, month, breed_mix, color_single, AnimalType_Dog, sex_male, neutered_neutered]

        prediction, probs = single_animal_prediction(feature_values, model_filename='gbc_model.joblib')
    
        prediction_string = ''.join(prediction)

        probs_dict = {'Return_to_owner':probs[0][3], 
              'Adoption':probs[0][0],
              'Transfer':probs[0][4],
              'Euthanasia':probs[0][2],
              'Died':probs[0][1]
            }

        prob_string = str(round(probs_dict[prediction_string] * 100, 1)) + '%'
        
        col1, col2 = st.columns(2)
        col1.metric('Predicted Outcome', prediction_string, help='Outcome predicted with Machine Learning, based on the values entered above.')

        col2.metric('Probability', prob_string, help='Probability of the predicted outcome for the animal.')    


with tab2:
    test = load_data('data/test.csv')
    drop_columns = ['SexuponOutcome', 'AgeuponOutcome']
    clean_data(test, drop_columns)
    drop_extra_columns = ['ID', 'Name', 'DateTime', 'Breed', 'Color', 'age_category']


    test_prepared = data_preparation(test, drop_extra_columns)

    model = load('gbc_model.joblib')

    predictions = model.predict(test_prepared)

    results = test.copy()
    results['OutcomeType'] = predictions

    # Filters and Metric

    col1, col2 = st.columns((2,1))
    with col1:
        animal_categories = results['AnimalType'].unique().tolist()
        animal_selection = st.multiselect('Choose animal types', animal_categories, animal_categories, key='A')
        results = results[results['AnimalType'].isin(animal_selection)]

    with col2:
        kpi_positive, kpi_returned, kpi_adopted, kpi_transferred, kpi_euthanized, kpi_died = calculate_metrics(results)

        st.metric("Positive Outcomes", str(kpi_positive) + "%", help='KPI representing the percentage of positive outcomes (return to owner or adoption).')

    # Plot Results

    category_orders=dict(OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])
    fig_predictions = px.histogram(results, x="OutcomeType", color='AnimalType', category_orders=category_orders)

    st.write(fig_predictions)

    # Metrics

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Returned to owner", str(kpi_returned) + "%", help='KPI representing the percentage of animals returned to their owner.')
    col2.metric("Adopted", str(kpi_adopted) + "%", help='KPI representing the percentage of animals that have been adopted.')
    col3.metric("Transferred", str(kpi_transferred) + "%", help="KPI representing the percentage of animals transferred to another shelter." )
    col4.metric("Euthanized", str(kpi_euthanized) + "%", help="KPI representing the percentage of animals that have been euthanized.")
    col5.metric("Died", str(kpi_died) + "%", help="KPI representing the percentage of animals that have died while staying at the shelter.")

    st.subheader('Sample Dataset')

    st.write(results)

with tab3:

    feat_importances = pd.read_csv('feat_importances.csv')
    importances_chart = px.bar(feat_importances, x='feature_name', y='importance')
    st.write(importances_chart)

    st.info('''
    
    When making a prediction with the machine learning model, the features that are the most important are:
    - Age in years (age_years)
    - If the animal has been neutered/spayed (neutered_neutered)
    - If the animal is a Dog or a Cat (AnimalType_Dog)
    - Month
    - If the animal is of a single color or not (color_single)
    - If the animal is male or female (sex_male)
    - If the animal is a mixed breed or not (breed_mix)

    ''')