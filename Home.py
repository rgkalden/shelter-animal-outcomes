
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


# Overall


category_orders = dict(
    OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])

fig_overall_outcomes = px.histogram(train, x="OutcomeType", color='AnimalType')
st.write(fig_overall_outcomes)

st.write(train)



