
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

from functions import *

st.set_page_config(page_title="Shelter Animal Outcomes", page_icon="🐾")

st.title("Shelter Animal Outcomes 🐾")

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

# Overall

fig_overall_outcomes = px.histogram(train, x="OutcomeType", color='AnimalType')
st.write(fig_overall_outcomes)

st.write(train)



