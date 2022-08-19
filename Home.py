
# # Shelter Animal Outcomes
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Shelter Animal Outcomes 🐾")

# ## Load Training Data




train = pd.read_csv('data/train.csv')



# ## Clean Training Data


def get_sex(string):
    string = str(string)
    if string.find('Male') >= 0: return 'male'
    if string.find('Female') >= 0: return 'female'
    return 'unknown'

def get_neutered(string):
    string = str(string)
    if string.find('Spayed') >= 0: return 'neutered'
    if string.find('Neutered') >= 0: return 'neutered'
    if string.find('Intact') >= 0: return 'intact'
    return 'unknown'


def calculate_age_years(age_string):

    age_string = str(age_string)
    if age_string == 'nan':
        return 0

    age = int(age_string.split()[0])

    if age_string.find('year') > -1:
        return age
    elif age_string.find('month') > -1:
        return age / 12
    elif age_string.find('week') > -1:
        return age / 52
    elif age_string.find('day') > -1:
        return age / 365


def age_category(age):
    if age < 3:
        return 'young'
    elif age >= 3 and age < 5:
        return 'middle'
    elif age >= 5 and age < 10:
        return 'adult'
    elif age >= 10:
        return 'old'


def clean_data(dataframe, drop_columns):
    dataframe['sex'] = dataframe['SexuponOutcome'].apply(get_sex)
    dataframe['neutered'] = dataframe['SexuponOutcome'].apply(get_neutered)

    dataframe['age_years'] = dataframe['AgeuponOutcome'].apply(calculate_age_years)

    dataframe['age_category'] = dataframe['age_years'].apply(age_category)

    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])

    dataframe.drop(drop_columns, axis=1, inplace=True)


drop_columns = ['SexuponOutcome', 'AgeuponOutcome', 'OutcomeSubtype']

clean_data(train, drop_columns)


#st.write(train)


# ## Visualizations


# ### Overall


#fig = px.histogram(train, x="AnimalType")
#fig.show()

category_orders=dict(OutcomeType=['Return_to_owner', 'Adoption', 'Transfer', 'Euthanasia', 'Died'])

fig_overall_outcomes = px.histogram(train, x="OutcomeType", color='AnimalType')
st.write(fig_overall_outcomes)


fig_overall_date = px.histogram(train[train['AnimalType'] == 'Cat'], x="DateTime", color='OutcomeType', category_orders=category_orders)
st.write(fig_overall_date)


# ### Breed


fig_breed = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType", color='Breed', category_orders=category_orders)
st.write(fig_breed)


top_breeds = train[train['AnimalType'] == 'Cat']['Breed'].value_counts()[:5].index.to_list()

#fig = px.histogram(train[train['Breed'].isin(top_breeds)], x="Breed")
#fig.show()


# ### Color


fig_color = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType", color='Color', category_orders=category_orders)
st.write(fig_color)


top_colors = train[train['AnimalType'] == 'Cat']['Color'].value_counts()[:5].index.to_list()

#fig = px.histogram(train[train['Color'].isin(top_colors)], x="Color")
#fig.show()


# ### Sex


fig_sex = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType", color='sex', category_orders=category_orders)
st.write(fig_sex)

#fig = px.histogram(train[train['AnimalType'] == 'Cat'], x="sex")
#fig.show()


# ### Neutered


fig_neutered = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType", color='neutered', category_orders=category_orders)
st.write(fig_neutered)


#fig = px.histogram(train[train['AnimalType'] == 'Cat'], x="neutered")
#fig.show()


# ### Age


fig_age = px.histogram(train[train['AnimalType'] == 'Cat'], x="OutcomeType", color='age_category', category_orders=category_orders)
st.write(fig_age)


#fig = px.histogram(train[train['AnimalType'] == 'Dog'], x='age_category')
#fig.show()





