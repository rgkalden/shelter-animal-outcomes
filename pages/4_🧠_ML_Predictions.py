import pandas as pd
import plotly.express as px
import streamlit as st
from joblib import load

from functions import *

st.title("ML Predictions")

with st.expander('About this Section'):
    st.write('Placeholder')



tab1, tab2 = st.tabs(['Batch Prediction', 'Single Animal Prediction'])

with tab1:
    test = load_data('data/test.csv')
    drop_columns = ['SexuponOutcome', 'AgeuponOutcome']
    clean_data(test, drop_columns)
    drop_extra_columns = ['ID', 'Name', 'DateTime', 'Breed', 'Color', 'age_category']


    test_prepared = data_preparation(test, drop_extra_columns)

    model = load('gbc_model.joblib')

    predictions = model.predict(test_prepared)

    results = test.copy()
    results['OutcomeType'] = predictions

    # Filters in Sidebar

    animal_categories = results['AnimalType'].unique().tolist()
    animal_selection = st.sidebar.multiselect('Choose animal types', animal_categories, animal_categories)
    results = results[results['AnimalType'].isin(animal_selection)]

    # Plot Results

    category_orders=dict(OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])
    fig_predictions = px.histogram(results, x="OutcomeType", color='AnimalType', category_orders=category_orders)

    st.write(fig_predictions)

    # Metrics

    kpi_positive, kpi_returned, kpi_adopted, kpi_transferred, kpi_euthanized, kpi_died = calculate_metrics(results)

    st.sidebar.metric("Positive Outcomes", str(kpi_positive) + "%", help='KPI representing the percentage of positive outcomes (return to owner or adoption).')

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Returned to owner", str(kpi_returned) + "%", help='KPI representing the percentage of animals returned to their owner.')
    col2.metric("Adopted", str(kpi_adopted) + "%", help='KPI representing the percentage of animals that have been adopted.')
    col3.metric("Transferred", str(kpi_transferred) + "%", help="KPI representing the percentage of animals transferred to another shelter." )
    col4.metric("Euthanized", str(kpi_euthanized) + "%", help="KPI representing the percentage of animals that have been euthanized.")
    col5.metric("Died", str(kpi_died) + "%", help="KPI representing the percentage of animals that have died while staying at the shelter.")

    st.subheader('Sample Dataset')

    st.write(results)

with tab2:

    col1, col2 = st.columns(2)
    with col1:
        # AnimalType_Dog

        animal_type = st.selectbox('Animal Type', ('Dog', 'Cat'), index=0)
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

        age_years = st.number_input('Age (years)', max_value=100., min_value=0., value=0.833)

    with col4:
        # month

        month = st.number_input('Month when outcome will occur (1-12)', min_value=1, max_value=12, step=1, value=10)


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

        neutered_bool = st.checkbox('Neutered', value=False)
        if neutered_bool:
            neutered_neutered = 1
        else:
            neutered_neutered = 0


    feature_values = [age_years, month, breed_mix, color_single, AnimalType_Dog, sex_male, neutered_neutered]

    prediction = single_animal_prediction(feature_values, model_filename='gbc_model.joblib')
    prediction_string = ''.join(prediction)

    st.metric('Predicted Outcome', prediction_string, help='Outcome predicted with Machine Learning, based on the values entered above.')