import streamlit as st
import requests
import pandas as pd
import datetime
import json
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()  #Load env variables from .env 
api_key = os.getenv("API_KEY")


#Google Trend Now
# Streamlit page configuration
st.set_page_config(page_title="Google Trends - Trending Now", layout="wide")

# Title and description
st.title(":cheese_wedge: What's Trending Now")
st.write("Explore the latest trending searches by customizing your region, time range, and language preferences.")

# Load region options from JSON file
with open("locations.json") as f:
    locations_data = json.load(f)
# Filter locations to include only those with 0, 1, or 2 letter codes
filtered_locations = {code: name for code, name in locations_data.items() if len(code) <= 2}

# User inputs for API parameters
geo_code = st.selectbox("Select Region:", options=list(filtered_locations.keys()), index=0, format_func=lambda x: filtered_locations[x])
hours = st.selectbox("Select Time Range (in hours):", options=['4', '24', '48', '168'], index=3)
language_code = "en"

# API endpoint with user-selected parameters
api_url_now = f"https://serpapi.com/search?engine=google_trends_trending_now&hours={hours}&geo={geo_code}&hl={language_code}&api_key={api_key}"

# Make the GET request to the API
response_now = requests.get(api_url_now)

# Check if the request was successful
if response_now.status_code == 200:
    # Parse the response JSON
    data_now = response_now.json()
    
    # Display raw JSON data
    #st.write("### Raw Data JSON Structure:")
    #st.json(data_now)  # Display JSON data for inspection
    
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
        #st.write("### Trending Searches Data:")
        #st.dataframe(df_now)
        
        # Process data function
        def data_process(data_df):
            data_df = data_df.copy()
            if 'start_timestamp' in data_df.columns:
                data_df['start_timestamp'] = data_df['start_timestamp'].map(lambda x: datetime.datetime.fromtimestamp(x) if pd.notna(x) else x)
            if 'end_timestamp' in data_df.columns:
                data_df['end_timestamp'] = data_df['end_timestamp'].map(lambda x: datetime.datetime.fromtimestamp(x) if pd.notna(x) else x)
            return data_df

        # Apply processing to the DataFrame
        processed_df_now = data_process(df_now)
        
        #st.write("### Processed Data:")
        #st.dataframe(processed_df_now)
        
        
        # Visualization - Sunburst Chart of Trends
        if 'query' in processed_df_now.columns and 'increase_percentage' in processed_df_now.columns and 'search_volume' in processed_df_now.columns:
            fig = px.sunburst(
                processed_df_now,
                path=['query'],
                color='increase_percentage',
                values='search_volume',
                template='seaborn',
                title="Trending Searches in Sunburst View"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for creating a sunburst chart.")

                # Top 5 Most Searched Queries - Histogram
        if 'query' in processed_df_now.columns and 'search_volume' in processed_df_now.columns:
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
            st.warning("Insufficient data for creating a histogram.")
else:
    # Error handling for unsuccessful API requests
    st.error(f"Failed to retrieve data from the API. Status code: {response_now.status_code}")
    st.write("Response text:", response_now.text)