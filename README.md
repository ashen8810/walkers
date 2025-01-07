# Tea Leaves Prediction Project

This project aims to predict the quantity of tea leaves using various regression models. The dataset includes features such as total tea leaves, rainfall, holidays, and date-related features.

## Overview

The main objective of this project is to forecast the amount of tea leaves based on historical data. The dataset includes the following features:
- `Total_Tea_Leaves`: The total quantity of tea leaves.
- `Rainfall`: The amount of rainfall.
- `Holiday`: Indicator if the day is a holiday.
- `Date`: The date of the record.

The project explores several machine learning models, including LightGBM, Gradient Boosting, Random Forest, and CatBoost regressors.

## Results
The RMSE for each model is as follows:

- LightGBM Regressor: RMSE: 10899.06
- Gradient Boosting Regressor: RMSE: 10794.87
- Random Forest Regressor: RMSE: 11017.74
- CatBoost Regressor: RMSE: 10477.19 (best result)

The CatBoost Regressor provides the best performance with the lowest RMSE.

## Flask API Application

This repository also includes a Flask application that serves as an API for predicting tea leaves quantities based on input data. You can use the API to make predictions using trained models.

## Conclusion
This project demonstrates the use of different regression models to predict the quantity of tea leaves. The CatBoost Regressor was found to be the most effective model in this case.

Feel free to contribute to this project by adding more features or improving the model performance.
