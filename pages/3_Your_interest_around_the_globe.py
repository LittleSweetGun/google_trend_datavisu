import streamlit as st
import requests
import pandas as pd
import datetime
import json
import plotly.express as px

#Google Trend Query Over Time
#Page configuration
st.set_page_config(page_title="Google Trends - Your interest around the globe", layout="wide")

# Title and description
st.title(":world_map: Your interest around the globe")
st.write("Ajouter texte explicatif")

#Load date and language data from SON file
with open("date.json") as f:
    date_data = json.load(f)
# Creating a dictionary for language codes and names
date_options = {da['date_code']: da['date_name'] for da in date_data}

with open("languages.json") as f:
    languages_data = json.load(f)
# Creating a dictionary for language codes and names
languages_options = {lang['language_code']: lang['language_name'] for lang in languages_data}

                   
#Search parameters by country
api_key = "b7744032f87d7c0a831939f9ce1b7f2402a47a9d03761ddcf577bfc5f3f290ac"

engine = 'google_trends'
language_code = st.selectbox("Select Language:", options=list(languages_options.keys()), index=1, format_func=lambda x: languages_options[x])
region = 'COUNTRY'
date_code = st.selectbox("Select Time Range:", options=list(date_options.keys()), index=1, format_func=lambda x: date_options[x])
data_type = 'GEO_MAP_0'
query = st.text_input('Your IOTD (Interest Of The Day)')
st.write(':blue[This works only for single query!]')

if query:
    api_url_country = f"https://serpapi.com/search.json?engine={engine}&q={query}&region={region}&hl={language_code}&date={date_code}&data_type={data_type}&api_key={api_key}"

    # Make the GET request to the API
    response_country = requests.get(api_url_country)

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