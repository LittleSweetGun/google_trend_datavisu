import streamlit as st
import requests
import pandas as pd
import datetime
import json
import plotly.express as px

#Google Trend Query Over Time
#Page configuration
st.set_page_config(page_title="Google Trends - Your interest over time", layout="wide")

# Title and description
st.title(":clock2: Your interest over time")
st.write("Ajouter texte explicatif")

# Load region options from JSON file
with open("locations.json") as f:
    locations_data = json.load(f)
# Filter locations to include only those with 0, 1, or 2 letter codes
filtered_locations = {code: name for code, name in locations_data.items() if len(code) <= 2}

with open("date.json") as f:
    date_data = json.load(f)
# Creating a dictionary for language codes and names
date_options = {da['date_code']: da['date_name'] for da in date_data}

#API parameters
api_key = "b7744032f87d7c0a831939f9ce1b7f2402a47a9d03761ddcf577bfc5f3f290ac"

engine = 'google_trends'
geo_code = st.selectbox("Select Region:", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
date_code = st.selectbox("Select Time Range:", options=list(date_options.keys()), index=1, format_func=lambda x: date_options[x])
query = st.text_input('Your IOTD (Interest Of The Day)')
st.write(':blue[It works only for single query, feel free to experiment!]')

# Only display if query is not empty
if query:
    
    # Construct API URL
    #Over time
    api_url_time = f"https://serpapi.com/search.json?engine={engine}&q={query}&hl=en&geo={geo_code}&date={date_code}&data_type=TIMESERIES&api_key={api_key}"
    #Around the world
    api_url_country = f"https://serpapi.com/search.json?engine={engine}&q={query}&region=COUNTRY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
    #Around a country
    api_url_city = f"https://serpapi.com/search.json?engine={engine}&q={query}&geo={geo_code}&region=CITY&hl=en&date={date_code}&data_type=GEO_MAP_0&api_key={api_key}"
     
    # Make the GET request to the API
    response_time = requests.get(api_url_time)
    response_country = requests.get(api_url_country)
    response_city = requests.get(api_url_city)

    # Check if the request was successful
    if response_time.status_code == 200:
        # Parse the response JSON
        data_time = response_time.json()
    
        # Flatten and process the JSON data
        if isinstance(data_time, dict):
            try:
                df_time = pd.json_normalize(data_time)
            except Exception as e:
                st.error(f"Error normalizing data: {e}")
                df_time = None
        elif isinstance(data_time, list):
            df_time = pd.DataFrame(data_time)
        else:
            st.error("Unexpected data format. Unable to convert to DataFrame.")
            df_time = None
    
        # Display the DataFrame
        if df_time is not None:
            # Process data function
            df_time = pd.DataFrame(df_time['interest_over_time.timeline_data'][0])
            def data_process(data_df):
                data_df = data_df.copy()
                if 'values' in data_df.columns:
                    data_df['values'] = data_df['values'].map(lambda x: int(x[0]['value']) if isinstance(x, list) and len(x) > 0 and 'value' in x[0] else None)
                if 'timestamp' in data_df.columns:
                    data_df['timestamp'] = data_df['timestamp'].map(lambda x: datetime.datetime.fromtimestamp(int(x)) if pd.notna(x) else x)
                return data_df

            # Apply processing to the DataFrame
            processed_df_date = data_process(df_time)
        
            with st.expander(":clock2: Your interest over time"):
            # Visualization - Sunburst Chart of Trends
                if 'date' in processed_df_date.columns and 'values' in processed_df_date.columns:
                    fig = px.bar(processed_df_date, x='date', y='values', color='values', template='ggplot2', title="Your query over time in Bar View")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient data for creating a bar chart.")
    else:
        # Error handling for unsuccessful API requests
        st.error(f"Failed to retrieve data from the API. Status code: {response_time.status_code}")
        st.write("Response text:", response_time.text)

    # Check if the request was successful
    if response_country.status_code == 200:
        # Parse the response JSON
        data_country = response_country.json()
    
        # Flatten and process the JSON data
        if isinstance(data_country, dict):
            try:
                df_country = pd.json_normalize(data_country)
            except Exception as e:
                st.error(f"Error normalizing data: {e}")
                df_country = None
        elif isinstance(data_country, list):
            df_country = pd.DataFrame(data_country)
        else:
            st.error("Unexpected data format. Unable to convert to DataFrame.")
            df_country = None
    
        # Display the DataFrame
        if df_country is not None:
            # Process data function
            df_country = pd.DataFrame(df_country['interest_by_region'][0])
            
            with st.expander(":world_map: Your interest around the globe"):
            # Visualization - Sunburst Chart of Trends
                if 'location' in df_country.columns and 'value' in df_country.columns:
                    fig = px.choropleth(df_country, locations='location', locationmode='country names', color='value', template='seaborn', hover_name='location', hover_data='value', title='Your query on the map')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient data for creating a bar chart.")
    else:
        # Error handling for unsuccessful API requests
        st.error(f"Failed to retrieve data from the API. Status code: {response_country.status_code}")
        st.write("Response text:", response_country.text)

    # Check if the request was successful
    if response_city.status_code == 200:
        # Parse the response JSON
        data_city = response_city.json()
    
        # Flatten and process the JSON data
        if isinstance(data_city, dict):
            try:
                df_city = pd.json_normalize(data_city)
            except Exception as e:
                st.error(f"Error normalizing data: {e}")
                df_city = None
        elif isinstance(data_city, list):
            df_city = pd.DataFrame(data_city)
        else:
            st.error("Unexpected data format. Unable to convert to DataFrame.")
            df_city = None
    
        # Display the DataFrame
        if df_city is not None:
            # Process data function
            df_city = pd.DataFrame(df_city['interest_over_time.timeline_data'][0])
            def data_process(data_df):
                data_df = data_df.copy()
                if 'values' in data_df.columns:
                    data_df['values'] = data_df['values'].map(lambda x: int(x[0]['value']) if isinstance(x, list) and len(x) > 0 and 'value' in x[0] else None)
                if 'timestamp' in data_df.columns:
                    data_df['timestamp'] = data_df['timestamp'].map(lambda x: datetime.datetime.fromtimestamp(int(x)) if pd.notna(x) else x)
                return data_df

            # Apply processing to the DataFrame
            processed_df_date = data_process(df_time)
        
            with st.expander(":flag-cp: Your interest around a country :flag-cn: "):
            # Visualization - Sunburst Chart of Trends
                if 'date' in processed_df_date.columns and 'values' in processed_df_date.columns:
                    fig = px.bar(processed_df_date, x='date', y='values', color='values', template='ggplot2', title="Your query over time in Bar View")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient data for creating a bar chart.")
    else:
        # Error handling for unsuccessful API requests
        st.error(f"Failed to retrieve data from the API. Status code: {response_city.status_code}")
        st.write("Response text:", response_city.text)