import streamlit as st
import pandas as pd
import numpy as np
df = pd.read_csv('final_df2.csv')
institute_names = pd.read_csv('institute codes.csv')
institute_mapping = institute_names.set_index('code')['name'].to_dict()
df['Institute Name'] = df['institute_code'].map(institute_mapping)

st.image("seatalgo.png", use_column_width=True)

input_option = st.sidebar.radio("Choose Input Method", ("Percentile", "Merit No."))

# Input fields based on user choice
if input_option == "Percentile":
    percentile = st.sidebar.number_input("MHT-CET Percentile", value=None, placeholder="Enter your MHT-CET percentile")
    Merit = None
else:
    Merit = st.sidebar.number_input("MHT-CET Merit No.", value=None, placeholder="Enter your Merit Number")
    percentile = None

# Check if both inputs are provided
if percentile is not None and Merit is not None:
    st.error("Please provide only one input (Percentile or Merit No.)")

# Output based on user input
if percentile is not None:
    category = st.selectbox(
        "Select your Category: ",
        df['Category'].unique(),
        index=None,
        placeholder="Select Category",
    )
    st.write("You selected:", category)
    branch = st.multiselect(
        "Enter your preferred branch",
        np.sort(df['branch_name'].unique()),
        max_selections=5
    )
    if st.button("Submit", type="primary"):
        colleges = df['Institute Name'][(df['MHT-CET Score'] < percentile) & (df['Category'] == category) & (
                    df['branch_name'].isin(branch))].unique()
        if len(colleges) == 0:
            st.write("No colleges available.")
        else:
            st.write("Allotable Colleges:")
            for college in colleges:
                st.write(college)
                google_search_url = f"https://www.google.com/search?q={college.replace(' ', '+')}"
                st.info(f"[Show info about {college}]({google_search_url})")


elif Merit is not None:
    category = st.selectbox(
        "Select your Category: ",
        df['Category'].unique(),
        index=None,
        placeholder="Select Category",
    )
    st.write("You selected:", category)
    branch = st.multiselect(
        "Enter your preferred branch",
        np.sort(df['branch_name'].unique()),
        max_selections=5
    )
    if st.button("Submit", type="primary"):
        colleges = df['Institute Name'][(df['Merit No.'] < Merit) & (df['Category'] == category) & (
                    df['branch_name'].isin(branch))].unique()
        if len(colleges) == 0:
            st.write("No colleges available.")
        else:
            st.write("Allotable Colleges:")
            for college in colleges:
                st.write(college)
                google_search_url = f"https://www.google.com/search?q={college.replace(' ', '+')}"
                st.info(f"[Show info about {college}]({google_search_url})")

else:
    st.write("Please provide either MHT-CET percentile or Merit No.")
