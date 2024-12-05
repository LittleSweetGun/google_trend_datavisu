# Google Trends Data Visualization App

## Overview

This application provides a user-friendly platform to explore search trends from Google Trends in a visually engaging and insightful manner. Designed for marketers, researchers, students and curious users alike, this tool offers detailed insights into trending topics across various regions, timeframes and categories. Plotly library is used for all the charts.

## Features

### Key Functionalities

#### **Trending Now**

Access real-time trending searches worldwide or within a specific region.
Users can choose a country and the time period they are interested in.

**Countries list**
The database, named locations.json, is composed of regions' and countries' name and their code (it's a dictionary).
Only countries' name are here displayed to the user (which means it include only those with 0, 1, or 2 letter codes in the locations database)

**Time period list**
There is 4 periods options here : past 4 hours, past day, past 2 days & the past week.

**Visualization**
Two charts are proposed to the user:

- A sunburst chart (which acts like a pie chart here) to display all the most treeding search on Google for the chosen region and period. The user can compare the increase pourcentage of each query thanks to a color scheme (from dark to light);
- An histogram of the top 5 queries for the chosen region and period. The user can compare the increase pourcentage of each query thanks to a color scheme (from dark to light) here too.

**Fun fact**
Soccer/Football is always "hot" in France (every time we tried for this country, all the top queries were about this sport).

#### **Your IOTD**

Like the "Trending Now part", users can choose a region and a time period. Here, users have to write the query they are interest in (only single query for now) and click "enter" to fetch the data.

**Time period list**
This time, we created a database, named date.json, composed of a dictionnary of each period and its code.

**Feature explanations**
You can find some more information on this page about all the features (no need to read this READ.ME file to understand how this page work).

1. **Interest Over Time**  
   Analyze how a specific topic's popularity has evolved, with time-series data and trend forecasts.

   **Visualization**
   Users have to open the expander to see the line chart for the region, time period and query selected at the top of the page. If the time period selected is 1 or 3 months, a second line chart will be visible with forecasted data.

   **Explanation of Forecast chart**
   While trying to implement a forecast feature in the "Your query over time" visualization part, we observe that only predictions for the past month and the past three months were actually working.

- **Prediction method** : The prediction method used here is Prophet by Facebook. This method provides a more robust, adaptive alternative to LES by fitting models with trend and seasonality using Bayesian techniques and extends beyond Holt-Winters by supporting multiple seasonalities, holidays and other custom events in the model. Also, Prophet can handle missing data, outliers and custom seasonalities, which the other methods (especially LES and Holt-Winters) struggle with.
  - **Past hour,Past 4 hours,Past days** : Because there is too little data, we can only roughly predict one direction.There is no need to predict
  - **Past 7 days** : It only shows seasonality but no trend, so it is difficult to predict
  - **Past month, Past 3 months** : A "perfect" model that has both seasonal and trend characteristics, so we choose these two period to show future trends.
  - **Past year, Past 5 years,From 2004 to now** : Strong trend but no strong seasonality.

2. **Trend Around the world**  
    View how topics are trending globally with an interactive map.

   **Visualization**
   Users have to open the expander to see the choropleth chart for the time period and query selected at the top of the page.
   There, they can see which countries are interested is the same topic. Thank to its interectivity, they can also see the number of searchs when passing over the country they're interested in.

3. **Trend Around the US**  
    Explore search trends across major US cities to understand regional interest patterns.

   **Visualization**
   Users have to open the expander to see the scatter mapbox chart for the time period and query selected at the top of the page.
   There, they can see which cities in the US are interested is the same topic. Thank to its interectivity, they can also see the number of searchs when passing over the city they're interested in.

   **Information**
   This part is sometimes working but other times not. We didn't find a solution for now.

### Data Visualization Tools

- **Interactive Sunburst Charts** to explore trends by hierarchy.
- **Bar Charts** for identifying top queries.
- **Line Charts** illustrating trends over time.
- **Maps** showcasing geographic hotspots of search activity.

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
