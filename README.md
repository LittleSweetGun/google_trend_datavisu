# Google Trends Data Visualization App

## Overview

This application provides a user-friendly platform to explore search trends from Google Trends in a visually engaging and insightful manner. Designed for marketers, researchers and curious users alike, this tool offers detailed insights into trending topics across various regions, timeframes, and categories.

## Features

### Key Functionalities

1. **Trending Now**  
   Access real-time trending searches worldwide or within a specific region.
2. **Trend Around the US**  
   Explore search trends across major US cities to understand regional interest patterns (this part is not always working).
3. **Trend Around the world**  
   View how topics are trending globally with interactive heatmaps and geographic visualizations.
4. **Interest Over Time**  
   Analyze how a specific topic's popularity has evolved, with time-series data and trend forecasts.

   #### Explanation of Forecast charts

   While trying to implement a forecast feature in the "Your query over time" visualization part, we observe that only predictions for the past month and the past three months were actually working.

- **Prediction method** : The prediction method used here is Prophet by Facebook. This method provides a more robust, adaptive alternative to LES by fitting models with trend and seasonality using Bayesian techniques and extends beyond Holt-Winters by supporting multiple seasonalities, holidays and other custom events in the model. Also, Prophet can handle missing data, outliers and custom seasonalities, which the other methods (especially LES and Holt-Winters) struggle with.

- **Past hour,Past 4 hours,Past days** : Because there is too little data, we can only roughly predict one direction.There is no need to predict

- **Past 7 days** : It only shows seasonality but no trend, so it is difficult to predict

- **Past month, Past 3 months** : A "perfect" model that has both seasonal and trend characteristics, so we choose these two period to show future trends.

- **Past year, Past 5 years,From 2004 to now** : Strong trend but no strong seasonality.

### Data Visualization Tools

- **Interactive Sunburst Charts** to explore trends by hierarchy.
- **Bar Charts** for identifying top queries.
- **Maps** showcasing geographic hotspots of search activity.
- **Line Charts** illustrating trends over time.

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.7+
- Streamlit
- Plotly
- Pandas
- requests

## How to Use

1. **Navigate the Sections**  
   Use the sidebar to switch between "Homepage", "Trending Now" and "Your IOTD"

2. **Customize Your View**  
   Input regions, timeframes and topics of interest to tailor the analysis.

3. **Visualize Trends**  
   Explore data through various charts, from sunburst views to time-series plots.

4. **Interact with Data**  
   Use interactive visualizations to drill down into specific areas of interest.

## Data Source

This application uses data from the following APIs:

- [SerpAPI Google Trends API](https://serpapi.com/google-trends-api)
- [SerpAPI Google Trends Trending Now API](https://serpapi.com/google-trends-trending-now)

Trends reflect real-time and historical search patterns as provided by SerpAPI.
