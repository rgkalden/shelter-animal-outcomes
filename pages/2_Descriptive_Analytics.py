import pandas as pd
import plotly.express as px
import streamlit as st

from functions import *

train = load_data('data/train.csv')

drop_columns = ['SexuponOutcome', 'AgeuponOutcome', 'OutcomeSubtype']

clean_data(train, drop_columns)

category_orders = dict(
    OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])

# Date


fig_overall_date = px.histogram(train[train['AnimalType'] == 'Cat'],
                                x="DateTime", color='OutcomeType', category_orders=category_orders)
st.write(fig_overall_date)


# Breed


fig_breed = px.histogram(train[train['AnimalType'] == 'Cat'],
                         x="OutcomeType", color='Breed', category_orders=category_orders)
st.write(fig_breed)


top_breeds = train[train['AnimalType'] == 'Cat']['Breed'].value_counts()[
    :5].index.to_list()

#fig = px.histogram(train[train['Breed'].isin(top_breeds)], x="Breed")
# fig.show()


# Color


fig_color = px.histogram(train[train['AnimalType'] == 'Cat'],
                         x="OutcomeType", color='Color', category_orders=category_orders)
st.write(fig_color)


top_colors = train[train['AnimalType'] == 'Cat']['Color'].value_counts()[
    :5].index.to_list()

#fig = px.histogram(train[train['Color'].isin(top_colors)], x="Color")
# fig.show()


# Sex


fig_sex = px.histogram(train[train['AnimalType'] == 'Cat'],
                       x="OutcomeType", color='sex', category_orders=category_orders)
st.write(fig_sex)

#fig = px.histogram(train[train['AnimalType'] == 'Cat'], x="sex")
# fig.show()


# Neutered


fig_neutered = px.histogram(train[train['AnimalType'] == 'Cat'],
                            x="OutcomeType", color='neutered', category_orders=category_orders)
st.write(fig_neutered)


#fig = px.histogram(train[train['AnimalType'] == 'Cat'], x="neutered")
# fig.show()


# Age


fig_age = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType",
                       color='age_category', category_orders=category_orders)
st.write(fig_age)


#fig = px.histogram(train[train['AnimalType'] == 'Dog'], x='age_category')
# fig.show()
