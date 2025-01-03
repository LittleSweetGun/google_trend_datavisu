import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px

from module import data_process_now

#API_KEY secret from .env for github
#import os
#from dotenv import load_dotenv
#load_dotenv()  # Loads variables from .env file
#api_key = os.getenv("API_KEY")

#API_KEY secret on streamlit
api_key = st.secrets["API_KEY"]


#Google Trend Now
# Streamlit page configuration
st.set_page_config(page_title="Google Trends - Trending Now", layout="wide")

# Title and description
st.title(":cheese_wedge: What's Trending Now")
st.write("Explore the latest trending searches by customizing your country and time range preferences. Let's dive into the current buzz! :v:")

# Load region options from JSON file
with open("locations.json") as f:
    locations_data = json.load(f)
# Filter locations to include only those with 0, 1, or 2 letter codes
filtered_locations = {code: name for code, name in locations_data.items() if len(code) <= 2}

# User inputs for API parameters
geo_code = st.selectbox("🚀 :blue[**Where ?**]", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
hours = st.selectbox("⌛ :blue[**When ?** (in hours)]", options=['4', '24', '48', '168'], index=3)
language_code = "en"

# API endpoint with user-selected parameters
api_url_now = f"https://serpapi.com/search?engine=google_trends_trending_now&hours={hours}&geo={geo_code}&hl={language_code}&api_key={api_key}"

#Make the GET request to the API
#Not using fetch_data function because it's too slow for here (didn't find the reason why)
response_now = requests.get(api_url_now)

# Check if the request was successful
if response_now.status_code == 200:
    data_now = response_now.json()
    
    # Flatten and process the JSON data
    if isinstance(data_now, dict) and 'trending_searches' in data_now:
        try:
            df_now = pd.json_normalize(data_now['trending_searches'])
        except Exception as e:
            st.error(f"Error normalizing data: {e}")
            df_now = None
    elif isinstance(data_now, list):
        df_now = pd.DataFrame(data_now)
    else:
        st.error("Unexpected data format. Unable to convert to DataFrame.")
        df_now = None
    
    # Display the DataFrame
    if df_now is not None:
        # Apply processing to the DataFrame
        processed_df_now = data_process_now(df_now)
        
        if 'query' in processed_df_now.columns and 'increase_percentage' in processed_df_now.columns and 'search_volume' in processed_df_now.columns:
            # Visualization of all - Sunburst Chart of Trends
            fig = px.sunburst(
                processed_df_now,
                path=['query'],
                color='increase_percentage',
                values='search_volume',
                template='seaborn',
                title="Trending Searches in Sunburst View"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            #Top 5 Most Searched Queries - Histogram
            top_5_df = processed_df_now.nlargest(5, 'search_volume')[['query', 'search_volume']]
            hist_fig = px.bar(
                top_5_df,
                x='query',
                y='search_volume',
                title="Top 5 Most Searched Queries",
                color='search_volume',
                template='seaborn'
            )
            hist_fig.update_layout(
                xaxis=dict(showticklabels=True, title=None),
                yaxis=dict(showticklabels=True, title=None),
                showlegend=False
            )
            st.plotly_chart(hist_fig, use_container_width=True)
        else:
            st.warning("Insufficient data for creating a sunburst chart.")

else:
    # Error handling for unsuccessful API requests
    st.error(f"Failed to retrieve data from the API. Status code: {response_now.status_code}")
    st.write("Response text:", response_now.text)