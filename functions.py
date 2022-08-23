
import pandas as pd

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
