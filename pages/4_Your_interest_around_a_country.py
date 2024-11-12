import streamlit as st
import requests
import pandas as pd
import datetime
import json
import plotly.express as px

#Google Trend Query Over Time
#Page configuration
st.set_page_config(page_title="Google Trends - Your interest around a country", layout="wide")

# Title and description
st.title(":flag-cp: Your interest around a country :flag-cn: ")
st.write("Ajouter texte explicatif")

# Load language options from JSON file
with open("languages.json") as f:
    languages_data = json.load(f)
# Creating a dictionary for language codes and names
languages_options = {lang['language_code']: lang['language_name'] for lang in languages_data}

# Load region options from JSON file
with open("locations.json") as f:
    locations_data = json.load(f)
# Filter locations to include only those with 0, 1, or 2 letter codes
filtered_locations = {code: name for code, name in locations_data.items() if len(code) <= 2}

with open("date.json") as f:
    date_data = json.load(f)
# Creating a dictionary for language codes and names
date_options = {da['date_code']: da['date_name'] for da in date_data}


#Search parameters compared by city
api_key = "b7744032f87d7c0a831939f9ce1b7f2402a47a9d03761ddcf577bfc5f3f290ac"

engine = 'google_trends'
language_code = st.selectbox("Select Language:", options=list(languages_options.keys()), index=1, format_func=lambda x: languages_options[x])
geo_code = st.selectbox("Select Region:", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
region = 'CITY'
date_code = st.selectbox("Select Time Range:", options=list(date_options.keys()), index=1, format_func=lambda x: date_options[x])
tz = '420' #time zone
data_type = 'GEO_MAP_0'
query = st.text_input('Your IOTD (Interest Of The Day)')
st.write(':blue[This works only for single query!]')

if query:
    api_url_city = f"https://serpapi.com/search.json?engine={engine}&q={query}&geo={geo_code}&region={region}&hl={language_code}&date={date_code}&data_type={data_type}&api_key={api_key}"
         
    # Make the GET request to the API
    response_city = requests.get(api_url_city)

    # Check if the request was successful
    if response_city.status_code == 200:
        # Parse the response JSON
        data_city = response_city.json()
    
        # Flatten and process the JSON data
        if isinstance(data_city, dict):
            try:
                df_time = pd.json_normalize(data_city)
            except Exception as e:
                st.error(f"Error normalizing data: {e}")
                df_time = None
        elif isinstance(data_city, list):
            df_time = pd.DataFrame(data_city)
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