import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Seat Algo", layout="wide", initial_sidebar_state="collapsed")

# Define introduction page
def introduction_page():
    st.image("seatalgo.png", width=300)
    st.write("""
        Welcome to the Seat Allocation System!
        
        Guess no more, which college you will get is predicted by our model. 
        Check your Seat allocation status right now by clicking the below button.
    """)
    if st.button("Next"):
        st.session_state.page = "main_project"

# Define main project page
def main_project():
    df = pd.read_csv('final_df2.csv')
    institute_names = pd.read_csv('institute codes.csv')
    institute_mapping = institute_names.set_index('code')['name'].to_dict()
    df['Institute Name'] = df['institute_code'].map(institute_mapping)
    st.image("seatalgo.png",  width=300)

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

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "introduction"

# Render pages based on session state
if st.session_state.page == "introduction":
    introduction_page()
elif st.session_state.page == "main_project":
    main_project()
