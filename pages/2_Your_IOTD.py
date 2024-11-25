import streamlit as st
import pandas as pd
import json
import plotly.express as px

from prophet import Prophet

from module import (fetch_data, data_process_city, data_process_time)


#API_KEY secret from .env for github
import os
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env file
api_key = os.getenv("API_KEY")

#API_KEY secret on streamlit
#api_key = st.secrets["API_KEY"]



st.set_page_config(page_title="Google Trends - Your IOTD ✨", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>✨ WhaT's Vibing Today ✨</h1>", unsafe_allow_html=True)
st.write("This web page is your ultimate __trend-spotting__ superpower, letting you track the evolution of your interests in real-time—because who doesn’t want to know where in the world (or even the US) people are vibing to the same thing you are? 😎")

# Features Section
st.subheader("🏗️ Features")
st.write(":blue[**Interest Over Time**]") 
st.write("You can input your Interest of the Day (IOTD) and see how it’s been trending over time. It’s like Google Trends, but with way more personality. Want to know if your new obsession is just a flash in the pan or the next big thing? We’ve got you covered with time-series data and forecasts 🔮")

st.write(":blue[**Global Interest:**]")
st.write("See where your topic is blowing up around the world 🌍 Is it trending in France ? Maybe in Japan? A map shows the hotspots, so you can feel extra cool knowing exactly where people are Googling what you’re into 🌎✨")

st.write(":blue[**US City Trends:**]")
st.write("Curious where in the US people are losing their minds over the same thing? Check out city-level search data. You might be surprised to see which city is leading the pack—it could be your hometown, where you went on holidays or somewhere totally random! 🏙️🔥")

st.subheader("🤿 Start diving!")
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
geo_code = st.selectbox("🚀 :blue[**Where ?**]", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
date_code = st.selectbox("⌛ :blue[**When ?**]", options=list(date_options.keys()), index=1, format_func=lambda x: date_options[x])
st.write(':gray[**Feature** : Forecasts available for one and three months]')
query = st.text_input('🔥 :blue[**Your IOTD (Interest Of The Day)**]')
st.write('🚨 :gray[ It only works for single queries!!]')

#Only display if query is not empty (after enter)
if query:
    
    #Construct API URL
    #Over time
    api_url_time = f"https://serpapi.com/search.json?engine={engine}&q={query}&hl=en&geo={geo_code}&date={date_code}&data_type=TIMESERIES&api_key={api_key}"
    #Around the world
    api_url_country = f"https://serpapi.com/search.json?engine={engine}&q={query}&region=COUNTRY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
    #Around a country
    api_url_city = f"https://serpapi.com/search.json?engine={engine}&q={query}&geo=US&region=CITY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
    
    #Fetch data
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
            if 'ds' in processed_df_date.columns and 'y' in processed_df_date.columns:
                fig_actual = px.line(processed_df_date, x='ds', y='y', template='seaborn', title=f"Search Trends for '{query}'")
                st.plotly_chart(fig_actual, use_container_width=True)

                # Only perform forecasting if time range is "past 3 months" or "past month"
                if date_code in ['today 1-m', 'today 3-m']:
                # Forecasting with Prophet
                    model = Prophet()
                    model.fit(processed_df_date)

                    # Predict future data
                    future = model.make_future_dataframe(periods=30)  # Predict the next 30 days
                    forecast = model.predict(future)

                    # Combine actual and forecasted data for visualization
                    forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
                    combined_df = pd.merge(processed_df_date, forecast_filtered, on='ds', how='outer')

                    # Visualization: Actual and Forecast Combined
                    fig_combined = px.line(combined_df, x='ds', y='y', title=f"Actual and Forecasted Trends for '{query}'")
                    fig_combined.add_scatter(x=combined_df['ds'], y=combined_df['yhat'], mode='lines', name='Forecast')
                    fig_combined.add_scatter(x=combined_df['ds'], y=combined_df['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot'))
                    fig_combined.add_scatter(x=combined_df['ds'], y=combined_df['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot'))
                    st.plotly_chart(fig_combined, use_container_width=True)
            else:
                st.warning("Insufficient data for creating a line chart.")
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