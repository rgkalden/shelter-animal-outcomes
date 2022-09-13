import numpy as np
import pandas as pd
from joblib import load


def load_data(filename):
    '''
    Function to load data from csv file into pandas DataFrame

    Parameters:
    filename - path to csv file

    Returns:
    DataFrame

    '''
    return pd.read_csv(filename)


def get_sex(string):
    '''
    Function to extract the sex from a string located in a pandas series.
    To be used in the pandas apply function.

    Parameters:
    string - string to be parsed

    Returns:
    string, either 'male' or 'female'

    '''
    string = str(string)
    if string.find('Male') >= 0:
        return 'male'
    if string.find('Female') >= 0:
        return 'female'
    return 'unknown'


def get_neutered(string):
    '''
    Function to extract whether an animal has been neutered or spayed
    from a string located in a pandas series.
    To be used in the pandas apply function.

    Parameters:
    string - string to be parsed

    Returns:
    string

    '''
    string = str(string)
    if string.find('Spayed') >= 0:
        return 'neutered'
    if string.find('Neutered') >= 0:
        return 'neutered'
    if string.find('Intact') >= 0:
        return 'intact'
    return 'unknown'


def calculate_age_years(age_string):
    '''
    Function to extract the age from a string located in a pandas series.
    To be used in the pandas apply function.

    Parameters:
    age_string - string to be parsed

    Returns:
    age - float value of age in years

    '''

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
    '''
    Function to place an animal into a certain predefined age category,
    based on its age in years.
    To be used with pandas apply function.

    Parameters:
    age - series containing ages in years

    Returns:
    string - string represting age category

    '''
    if age < 3:
        return 'young'
    elif age >= 3 and age < 5:
        return 'middle'
    elif age >= 5 and age < 10:
        return 'adult'
    elif age >= 10:
        return 'old'


def clean_data(dataframe, drop_columns):
    '''
    Function to clean data from dataframe

    Parameters:
    dataframe - dataframe to clean
    drop_columns - columns to remove (drop)

    Returns:
    None (dataframe modified in place)

    '''
    dataframe['sex'] = dataframe['SexuponOutcome'].apply(get_sex)
    dataframe['neutered'] = dataframe['SexuponOutcome'].apply(get_neutered)

    dataframe['age_years'] = dataframe['AgeuponOutcome'].apply(
        calculate_age_years)

    dataframe['age_category'] = dataframe['age_years'].apply(age_category)

    dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'])

    dataframe.drop(drop_columns, axis=1, inplace=True)


def calculate_metrics(dataframe):
    '''
    Function to calculate key metrics/KPI's related to the animal shelter.
    Used prior to being displayed with the streamlit metric function.

    Parameters:
    dataframe - contains data that metrics will be calculated on

    Returns:
    kpi_positive, kpi_returned, kpi_adopted, 
        kpi_transferred, kpi_euthanized, kpi_died - metric values
    '''

    num_positive = len(
        dataframe[dataframe['OutcomeType'].isin(['Return_to_owner', 'Adoption'])])
    kpi_positive = round(num_positive / len(dataframe) * 100, 1)

    num_returned = len(
        dataframe[dataframe['OutcomeType'].isin(['Return_to_owner'])])
    kpi_returned = round(num_returned / len(dataframe) * 100, 1)

    num_adopted = len(dataframe[dataframe['OutcomeType'].isin(['Adoption'])])
    kpi_adopted = round(num_adopted / len(dataframe) * 100, 1)

    num_transferred = len(
        dataframe[dataframe['OutcomeType'].isin(['Transfer'])])
    kpi_transferred = round(num_transferred / len(dataframe) * 100, 1)

    num_euthanized = len(
        dataframe[dataframe['OutcomeType'].isin(['Euthanasia'])])
    kpi_euthanized = round(num_euthanized / len(dataframe) * 100, 1)

    num_died = len(dataframe[dataframe['OutcomeType'].isin(['Died'])])
    kpi_died = round(num_died / len(dataframe) * 100, 1)

    return kpi_positive, kpi_returned, kpi_adopted, kpi_transferred, kpi_euthanized, kpi_died


def get_month(timestamp):
    '''
    Function to get the month from a pandas timestamp.
    Used within the pandas apply function.

    Parameters:
    timestamp - pandas TimeStamp

    Returns:
    integer for the month

    '''
    return timestamp.month


def get_breed_mix(string):
    '''
    Function to determine whether the animal is a mixed breed.
    Used within the pandas apply function.

    Parameters:
    string - string within pandas series representing the breed

    Returns:
    integer - 1 for Mix, 0 for pure breed

    '''
    string = str(string)
    if string.find('Mix') >= 0 or string.find('/') >= 0:
        return 1
    else:
        return 0


def get_single_color(string):
    '''
    Function to determine whether the animal is a single color.
    Used within the pandas apply function.

    Parameters:
    string - string within pandas series representing the color

    Returns:
    integer - 1 for single color, 0 for mixed color

    '''
    string = str(string)
    if string.find('/') >= 0:
        return 0
    else:
        return 1


def data_preparation(df, drop_extra_columns):
    '''
    Function to prepare data for machine learning.

    Parameters:
    df - dataframe containing prepared data
    drop_extra_columns - list of columns to be dropped

    Returns:
    dataframe - dataframe with prepared data

    '''

    dataframe = df.copy()

    dataframe['month'] = dataframe['DateTime'].apply(get_month)

    dataframe['breed_mix'] = dataframe['Breed'].apply(get_breed_mix)

    dataframe['color_single'] = dataframe['Color'].apply(get_single_color)

    dataframe.drop(drop_extra_columns, axis=1, inplace=True)

    dataframe = pd.get_dummies(
        dataframe, columns=['AnimalType', 'sex', 'neutered'], drop_first=True)

    dataframe.drop(['sex_unknown', 'neutered_unknown'], axis=1, inplace=True)

    return dataframe


def single_animal_prediction(feature_values, model_filename):
    '''
    Function to predict the outcome for a single animal, using 
    a previously trained machine learning model. Used within
    a streamlit form which gathers the feature values.

    Parameters:
    feature_values - list containing feature values
    model_filename - path to joblib model file

    Returns:
    prediction - numpy array containing prediction for the outcome
    probs - numpy array with probabilities for each possible outcome

    '''
    feature_array = np.array(feature_values).reshape(1, -1)

    model = load(model_filename)

    prediction = model.predict(feature_array)

    probs = model.predict_proba(feature_array)

    return prediction, probs
