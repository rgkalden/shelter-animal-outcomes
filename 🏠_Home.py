
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

from functions import *

st.set_page_config(page_title="Shelter Animal Outcomes", page_icon="🐾")

st.title("Shelter Animal Outcomes 🐾")

with st.expander('About this Dashboard'):
    st.write('Placeholder')

# Load Training Data

train = load_data('data/train.csv')


# Clean Training Data


drop_columns = ['SexuponOutcome', 'AgeuponOutcome', 'OutcomeSubtype']

clean_data(train, drop_columns)


# Filters in Sidebar

datetime_min = train['DateTime'].min()
datetime_max = train['DateTime'].max()

start_date = st.sidebar.date_input("Start Date", datetime_min)
end_date = st.sidebar.date_input("End Date", datetime_max)


train = train[(train['DateTime'] >= pd.Timestamp(start_date)) & (train['DateTime'] <= pd.Timestamp(end_date))]

animal_categories = train['AnimalType'].unique().tolist()
animal_selection = st.sidebar.multiselect('Choose animal types', animal_categories, animal_categories)
train = train[train['AnimalType'].isin(animal_selection)]

# Overall

fig_overall_outcomes = px.histogram(train, x="OutcomeType", color='AnimalType')
st.write(fig_overall_outcomes)

kpi_positive, kpi_returned, kpi_adopted, kpi_transferred, kpi_euthanized, kpi_died = calculate_metrics(train)

st.sidebar.metric("Positive Outcomes", str(kpi_positive) + "%", help='KPI representing the percentage of positive outcomes (return to owner or adoption).')

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Returned to owner", str(kpi_returned) + "%", help='KPI representing the percentage of animals returned to their owner.')
col2.metric("Adopted", str(kpi_adopted) + "%", help='KPI representing the percentage of animals that have been adopted.')
col3.metric("Transferred", str(kpi_transferred) + "%", help="KPI representing the percentage of animals transferred to another shelter." )
col4.metric("Euthanized", str(kpi_euthanized) + "%", help="KPI representing the percentage of animals that have been euthanized.")
col5.metric("Died", str(kpi_died) + "%", help="KPI representing the percentage of animals that have died while staying at the shelter.")

st.subheader('Dataset')
st.write(train)



