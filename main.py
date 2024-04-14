import streamlit as st
import pandas as pd
import numpy as np

# Read data
df = pd.read_csv('final_df2.csv')
institute_names = pd.read_csv('institute codes.csv')
institute_mapping = institute_names.set_index('code')['name'].to_dict()
df['Institute Name'] = df['institute_code'].map(institute_mapping)

st.title("Seat Algo")

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
                if st.button(f"Show Location of {college}"):
                    st.write(f"Fetching coordinates for {college}...")
                    latitude, longitude = df.loc[df['Institute Name'] == college, ['latitude', 'longitude']].values[0]
                    if latitude is not None and longitude is not None:
                        map_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"
                        st.markdown(f'<iframe width="800" height="600" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{map_url}"></iframe>',
                                    unsafe_allow_html=True)
                    else:
                        st.error(f"Unable to find coordinates for {college}")

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
                if st.button(f"Show info about {college}"):
                    st.write(f"Redirecting to the Google search page for {college}...")
                    google_search_url = f"https://www.google.com/search?q={college}"
                    st.markdown(f'<a href="{google_search_url}" target="_blank">Click here for more info</a>', unsafe_allow_html=True)


else:
    st.write("Please provide either MHT-CET percentile or Merit No.")
