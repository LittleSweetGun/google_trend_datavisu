# google_trend_datavisu

Explication app

## Explanation of Forecast charts

While trying to implement a forecast feature in the "Your query over time" visualization part, we observe that only predictions for the past month and the past three months were actually working.

### Prediction method

The prediction method used here is Prophet by Facebook. This method provides a more robust, adaptive alternative to LES by fitting models with trend and seasonality using Bayesian techniques and extends beyond Holt-Winters by supporting multiple seasonalities, holidays and other custom events in the model.
Also, Prophet can handle missing data, outliers and custom seasonalities, which the other methods (especially LES and Holt-Winters) struggle with.

What follows is an explanation of the reasoning behind the absence of predictions for data from other time periods.

### Past hour,Past 4 hours,Past days

Because there is too little data, we can only roughly predict one direction.There is no need to predict

### Past 7 days

It only shows seasonality but no trend, so it is difficult to predict

### Past month, Past 3 months

A perfect model that has both seasonal and trend characteristics, so we choose these two period to show future trends.

### Past year, Past 5 years,From 2004 to now

Strong trend but not strong seasonality, no need for research.
