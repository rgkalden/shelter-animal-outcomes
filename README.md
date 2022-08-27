[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rgkalden-shelter-animal-outcomes--home-695057.streamlitapp.com/)

# Shelter Animal Outcomes 🐾

Welcome to the repository for the Shelter Animal Outcomes dashboard web app! 

## Introduction

The goal of this dashboard app is to develop the concept of how outcomes for shelter animals can be improved by using analytics and machine learning. KPI's for animal shelter performance along with descriptive analytics are used to provide a description of the historical animal outcomes
at the shelter. Diagnostic analytics are used to provide insight into what features of the animals lead to certain outcomes. Machine learning is used to make predictions for what the outcome will be for new animals that arrive at the shelter.

By applying analytics and machine learning capabilities into this dahboard app, it is hoped that the information about animal outcomes is presented in a way that allows animal shelter employees to better understand what is happening at their shelter and what leads to certain types of outcomes for the animals.

> In the future, it is planned to add a page for Predictive Analytics, to forecast animal outcomes in the future, to help the shelter plan for demands in advance.

## App Structure

The app is built with Streamlit, and consists of the following files:

* `🏠_Home.py`
* `pages\2_🔍_Diagnostic_Analytics.py`
* `pages\4_🧠_ML_Predictions.py`
* `functions.py`

The notebook `model_development.ipynb` contains Python code to explore the dataset and experiment with features before incorporating them into the actual app scripts. Data for this project is from a past Kaggle competition, located [here.](https://www.kaggle.com/competitions/shelter-animal-outcomes/overview)

* `data\train.csv`
* `data\test.csv`

## Run the App Locally

With Streamlit installed, a local server can be started to run the app with the following terminal command:

```
streamlit run 🏠_Home.py
```

## View the App on Streamlit Cloud

The app has been deployed to Streamlit cloud for all to see, and can be viewed at:

[https://rgkalden-shelter-animal-outcomes--home-695057.streamlitapp.com/](https://rgkalden-shelter-animal-outcomes--home-695057.streamlitapp.com/)