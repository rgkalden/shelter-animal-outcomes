import pandas as pd
import plotly.express as px
import streamlit as st

from functions import *

st.title('Diagnostic Analytics')

with st.expander('About this Section'):
    st.write('''
    
    In this section, data is presented in order to reveal any patterns in
    animal outcomes. Features of the data are shown to explore whether
    or not they influence the type of outcome.    
    
    ''')


# Load Training Data


train = load_data('data/train.csv')

drop_columns = ['SexuponOutcome', 'AgeuponOutcome', 'OutcomeSubtype']

# Clean Data

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
st.header('Date')

fig_overall_date = px.histogram(train,
                                x="DateTime", color='OutcomeType', category_orders=category_orders)
st.write(fig_overall_date)


# Breed
st.header('Breed')

fig_breed = px.histogram(train,
                        x="OutcomeType", color='Breed', category_orders=category_orders)
st.write(fig_breed)


top_breeds = train['Breed'].value_counts()[:5].index.to_list()
st.write('Most common breeds')
st.subheader(', '.join(top_breeds))




# Color
st.header('Color')

fig_color = px.histogram(train,
                         x="OutcomeType", color='Color', category_orders=category_orders)
st.write(fig_color)


top_colors = train['Color'].value_counts()[:5].index.to_list()
st.write('Most common colors')
st.subheader(', '.join(top_colors))


# Sex
st.header('Sex')

fig_sex = px.histogram(train,
                       x="OutcomeType", color='sex', category_orders=category_orders)
st.write(fig_sex)

num_male = len(train[train['sex'] == 'male'])
num_female = len(train[train['sex'] == 'female'])
num_unk = len(train) - num_male - num_female

col1, col2, col3 = st.columns(3)
col1.metric("Female", num_female)
col2.metric("Male", num_male)
col3.metric("Unknown", num_unk)


# Neutered
st.header('Neutered')

fig_neutered = px.histogram(train,
                            x="OutcomeType", color='neutered', category_orders=category_orders)
st.write(fig_neutered)

num_neutered = len(train[train['neutered'] == 'neutered'])
num_intact = len(train[train['neutered'] == 'intact'])
num_unk_neu = len(train) - num_neutered - num_intact

col1, col2, col3 = st.columns(3)
col1.metric("Neutered", num_neutered)
col2.metric("Intact", num_intact)
col3.metric("Unknown", num_unk_neu)


# Age
st.header('Age')

fig_age = px.histogram(train, x="OutcomeType",
                       color='age_category', category_orders=category_orders)
st.write(fig_age)

st.caption('''

Note: Age categories are defined as: 
< 3: young,
< 5: middle,
< 10: adult, > 10: old

''')


fig_age_category = px.histogram(train, x='age_category', color='AnimalType')
st.write(fig_age_category)
