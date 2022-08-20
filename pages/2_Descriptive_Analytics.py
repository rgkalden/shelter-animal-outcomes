import pandas as pd
import plotly.express as px
import streamlit as st

from functions import *

train = load_data('data/train.csv')

drop_columns = ['SexuponOutcome', 'AgeuponOutcome', 'OutcomeSubtype']

clean_data(train, drop_columns)

category_orders = dict(
    OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])

# Filters in Sidebar


datetime_min = train['DateTime'].min()
datetime_max = train['DateTime'].max()

start_date = st.sidebar.date_input("Start Date", datetime_min)
end_date = st.sidebar.date_input("End Date", datetime_max)


train = train[(train['DateTime'] >= pd.Timestamp(start_date)) & (train['DateTime'] <= pd.Timestamp(end_date))]

animal_categories = train['AnimalType'].unique().tolist()
animal_selection = st.sidebar.multiselect('Choose animal types', animal_categories, animal_categories)
train = train[train['AnimalType'].isin(animal_selection)]


# Date
st.subheader('Date')

fig_overall_date = px.histogram(train,
                                x="DateTime", color='OutcomeType', category_orders=category_orders)
st.write(fig_overall_date)


# Breed
st.subheader('Breed')

fig_breed = px.histogram(train,
                         x="OutcomeType", color='Breed', category_orders=category_orders)
st.write(fig_breed)


top_breeds = train['Breed'].value_counts()[
    :5].index.to_list()

#fig = px.histogram(train[train['Breed'].isin(top_breeds)], x="Breed")
# fig.show()


# Color
st.subheader('Color')

fig_color = px.histogram(train,
                         x="OutcomeType", color='Color', category_orders=category_orders)
st.write(fig_color)


top_colors = train['Color'].value_counts()[
    :5].index.to_list()

#fig = px.histogram(train[train['Color'].isin(top_colors)], x="Color")
# fig.show()


# Sex
st.subheader('Sex')

fig_sex = px.histogram(train,
                       x="OutcomeType", color='sex', category_orders=category_orders)
st.write(fig_sex)

#fig = px.histogram(train[train, x="sex")
# fig.show()


# Neutered
st.subheader('Neutered')

fig_neutered = px.histogram(train,
                            x="OutcomeType", color='neutered', category_orders=category_orders)
st.write(fig_neutered)


#fig = px.histogram(train[train, x="neutered")
# fig.show()


# Age
st.subheader('Age')

fig_age = px.histogram(train, x="OutcomeType",
                       color='age_category', category_orders=category_orders)
st.write(fig_age)

st.write('''

age_category 
< 3: young,
< 5: middle,
< 10: adult, > 10: old

''')


#fig = px.histogram(train[train['AnimalType'] == 'Dog'], x='age_category')
# fig.show()
