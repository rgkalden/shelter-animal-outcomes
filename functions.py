import numpy as np
import pandas as pd
from joblib import load

def load_data(filename):
    return pd.read_csv(filename)


def get_sex(string):
    string = str(string)
    if string.find('Male') >= 0:
        return 'male'
    if string.find('Female') >= 0:
        return 'female'
    return 'unknown'


def get_neutered(string):
    string = str(string)
    if string.find('Spayed') >= 0:
        return 'neutered'
    if string.find('Neutered') >= 0:
        return 'neutered'
    if string.find('Intact') >= 0:
        return 'intact'
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

    dataframe['age_years'] = dataframe['AgeuponOutcome'].apply(
        calculate_age_years)

    dataframe['age_category'] = dataframe['age_years'].apply(age_category)

    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])

    dataframe.drop(drop_columns, axis=1, inplace=True)


def calculate_metrics(dataframe):

    num_positive = len(dataframe[dataframe['OutcomeType'].isin(['Return_to_owner', 'Adoption'])])
    kpi_positive = round(num_positive / len(dataframe) * 100, 1)

    num_returned = len(dataframe[dataframe['OutcomeType'].isin(['Return_to_owner'])])
    kpi_returned = round(num_returned / len(dataframe) * 100, 1)

    num_adopted = len(dataframe[dataframe['OutcomeType'].isin(['Adoption'])])
    kpi_adopted = round(num_adopted / len(dataframe) * 100, 1)

    num_transferred = len(dataframe[dataframe['OutcomeType'].isin(['Transfer'])])
    kpi_transferred = round(num_transferred / len(dataframe) * 100, 1)

    num_euthanized = len(dataframe[dataframe['OutcomeType'].isin(['Euthanasia'])])
    kpi_euthanized = round(num_euthanized / len(dataframe) * 100, 1)

    num_died = len(dataframe[dataframe['OutcomeType'].isin(['Died'])])
    kpi_died = round(num_died / len(dataframe) * 100, 1)

    return kpi_positive, kpi_returned, kpi_adopted, kpi_transferred, kpi_euthanized, kpi_died

def get_quarter(timestamp):
    month = timestamp.month

    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    elif month <= 12:
        return 4

def get_month(timestamp):
    return timestamp.month

def get_breed_mix(string):
    string = str(string)
    if string.find('Mix') >= 0 or string.find('/') >= 0:
        return 1
    else:
        return 0

def get_single_color(string):
    string = str(string)
    if string.find('/') >= 0:
        return 0
    else:
        return 1

def data_preparation(df, drop_extra_columns):

    dataframe = df.copy()

    #dataframe['has_name'] = dataframe['Name']
    #dataframe['has_name'].fillna(0, inplace=True)
    #dataframe['has_name'] = dataframe['has_name'].apply(lambda x: 1 if x != 0 else x)

    #dataframe['quarter'] = dataframe['DateTime'].apply(get_quarter)

    dataframe['month'] = dataframe['DateTime'].apply(get_month)

    dataframe['breed_mix'] = dataframe['Breed'].apply(get_breed_mix)

    dataframe['color_single'] = dataframe['Color'].apply(get_single_color)

    dataframe.drop(drop_extra_columns, axis=1, inplace=True)

    dataframe = pd.get_dummies(dataframe, columns=['AnimalType', 'sex', 'neutered'], drop_first=True)

    dataframe.drop(['sex_unknown', 'neutered_unknown'], axis=1, inplace=True)

    return dataframe


def single_animal_prediction(feature_values, model_filename):
    feature_array = np.array(feature_values).reshape(1, -1)

    model = load(model_filename)

    prediction = model.predict(feature_array)

    return prediction