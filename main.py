# contents to be added here
import streamlit as st
import pandas as pd
df = pd.read_csv('final_df2.csv')
st.title("Seat Algo")

percentile = st.number_input("MHT-CET Percentile", value=None, placeholder="Enter your MHT-CET percentile")
Merit = st.number_input("MHT-CET Merit No.", value=None, placeholder="Enter your Merit Number")

options = st.multiselect(
    "Enter your preferred branch",
    df['branch_name'].unique()
)