import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("API_KEY")  # Access the API key


from module import (fetch_data, data_process_city, data_process_time)


st.set_page_config(page_title="Google Trends - Your IOTD ✨", layout="wide")
st.title("✨ Your Interest Of The Day ✨")
st.write("Ajouter texte explicatif")

#Load locations (countries) options from locations.json file
with open("locations.json", encoding="utf-8") as f:
    locations_data = json.load(f)
# Filter locations to include only those with 0, 1, or 2 letter codes (only the countries and not the region)
filtered_locations = {code: name for code, name in locations_data.items() if len(code) <= 2}

#Load dates options from date.json file
with open("date.json", encoding="utf-8") as f:
    date_data = json.load(f)
#Creating a dictionary for language codes and names
date_options = {da['date_code']: da['date_name'] for da in date_data}

#API parameters

engine = 'google_trends'
geo_code = st.selectbox("Select Region:", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
date_code = st.selectbox("Select Time Range:", options=list(date_options.keys()), index=1, format_func=lambda x: date_options[x])
st.write(':blue[**Feature** : Forecasts available for one and three months]')
query = st.text_input('Your IOTD (Interest Of The Day)')
st.write(':red[**Warning** :]:blue[ It only works for single queries]')

#Only display if query is not empty (after enter)
if query:
    
    #Construct API URL
    #Over time
    api_url_time = f"https://serpapi.com/search.json?engine={engine}&q={query}&hl=en&geo={geo_code}&date={date_code}&data_type=TIMESERIES&api_key={api_key}"
    #Around the world
    api_url_country = f"https://serpapi.com/search.json?engine={engine}&q={query}&region=COUNTRY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
    #Around a country
    api_url_city = f"https://serpapi.com/search.json?engine={engine}&q={query}&geo=US&region=CITY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
    
    df_time = fetch_data(api_url_time)
    df_country = fetch_data(api_url_country)
    df_city = fetch_data(api_url_city)
    
    #Over time
    if df_time is not None:
        #Process data function
        df_time = pd.DataFrame(df_time['interest_over_time.timeline_data'][0])
        #Apply processing to the DataFrame
        processed_df_date = data_process_time(df_time)
        
        with st.expander(":clock2: Your interest over time :clock2:"):
        #Visualization
            if 'date' in processed_df_date.columns and 'values' in processed_df_date.columns:
                fig = px.bar(processed_df_date, x='date', y='values', color='values', template='ggplot2')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data for creating a bar chart.")
    else:
        st.warning("The data is not available.")
    
    #Around the world
    if df_country is not None:
        #Process data function (selecting the good column and row > no cleaning needed)
        df_country = pd.DataFrame(df_country['interest_by_region'][0])
            
        with st.expander(":world_map: Your interest around the globe :world_map:"):
        #Visualization
            if 'location' in df_country.columns and 'value' in df_country.columns:
                fig = px.choropleth(df_country, locations='location', locationmode='country names', color='value', template='seaborn', hover_name='location', hover_data='value')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data for creating a bar chart.")
    else:
        st.warning("The data is not available.")

    #Around the US
    if df_city is not None and 'interest_by_region' in df_city.columns:
        #Process data function (retrieve latitude and longitude in coordinates column)
        df_city = pd.DataFrame(df_city['interest_by_region'][0])
        #Process the data
        processed_df_city = data_process_city(df_city)
        
        with st.expander(":flag-us: Your interest around the US :flag-us: "):
        # Visualization
            if 'lat' in processed_df_city.columns and 'lng' in processed_df_city.columns:
                fig = px.scatter_mapbox(processed_df_city, lat='lat', lon='lng', color='value',template='ggplot2',hover_name='location',zoom=0,mapbox_style="carto-positron")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data for creating a map.")
    else:
        st.warning("The data is not available.")