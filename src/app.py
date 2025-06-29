import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:3000/stats"  # Adjust if your server runs elsewhere

st.title("Public API Dashboard — Stats Viewer")

st.write("Fetching data from PostgREST API...")

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    if not data:
        st.warning("No data found.")
    else:
        # Convert JSON list of dicts to DataFrame
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.line_chart(df.set_index('label')['value'])
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
