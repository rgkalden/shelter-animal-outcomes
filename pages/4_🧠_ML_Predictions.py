import pandas as pd
import plotly.express as px
import streamlit as st
from joblib import load

from functions import *

st.title("ML Predictions")

test = load_data('data/test.csv')
drop_columns = ['SexuponOutcome', 'AgeuponOutcome']
clean_data(test, drop_columns)
drop_extra_columns = ['ID', 'Name', 'DateTime', 'Breed', 'Color', 'age_category']


test_prepared = data_preparation(test, drop_extra_columns)

model = load('gbc_model.joblib')

predictions = model.predict(test_prepared)

results = test.copy()
results['OutcomeType'] = predictions

category_orders=dict(OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])
fig_predictions = px.histogram(results, x="OutcomeType", color='AnimalType', category_orders=category_orders)

st.write(fig_predictions)

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