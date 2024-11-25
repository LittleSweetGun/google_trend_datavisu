import datetime
import pandas as pd
import requests
import streamlit as st
   
def fetch_data(url):  
    #GET request to the APIs
    response= requests.get(url)

    #Error management
    if response.status_code == 200:
        data = response.json()
    
        #Flatten the JSON data (to avoid format errors)
        if isinstance(data, dict):
            try:
                df = pd.json_normalize(data)
                return df
            except Exception as e:
                st.error(f"Error normalizing data: {e}")
                return None
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            return df
        else:
            st.error("Unexpected data format. Unable to convert to DataFrame.")
            return None
    else:
        #Error handling for unsuccessful API requests
        st.error(f"Failed to retrieve data from the API. Status code: {response.status_code}")
        st.write("Response text:", response.text)

def data_process_city(data_df):
    data_df = data_df.copy()
    if 'coordinates' in data_df.columns:
        data_df['lat'] = data_df['coordinates'].map(lambda x: x['lat'])
        data_df['lng'] = data_df['coordinates'].map(lambda x: x['lng'])
    return data_df

def data_process_time(data_df):
    data_df = data_df.copy()
    if 'values' in data_df.columns:
        data_df['values'] = data_df['values'].map(lambda x: int(x[0]['value']) if isinstance(x, list) and len(x) > 0 and 'value' in x[0] else None)
    if 'timestamp' in data_df.columns:
        data_df['timestamp'] = data_df['timestamp'].map(lambda x: datetime.datetime.fromtimestamp(int(x)) if pd.notna(x) else x)
    return data_df
