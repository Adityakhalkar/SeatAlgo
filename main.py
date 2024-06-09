import streamlit as st
import pandas as pd
import numpy as np
from pymongo import MongoClient
from streamlit_oauth import OAuth2Callback

# MongoDB Atlas connection
def get_db_connection():
    mongo_uri = "mongodb+srv://khalkaraditya8:Kt56eKS07mX5dSSD@seatalgo.p8zlmgq.mongodb.net/seatalgo?retryWrites=true&w=majority&appName=SeatAlgo"
    client = MongoClient(mongo_uri)
    db = client.seatalgo  # Replace 'seatalgo' with your database name
    return db

# Set up MongoDB collection
db = get_db_connection()
users_collection = db['users']

# Initialize OAuth2 callback
oauth = OAuth2Callback()

# Define introduction page
def introduction_page():
    st.markdown(
        """
        <style>
        .st-emotion-cache-1v0mbdj.e115fcil1 {
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image("seatalgo.png", width=300)
    st.header("Guess no more, :blue[College] selection is easy now.")
    st.header("Check your :red[Eligibility] status right now.")

    # Google login
    if not oauth.logged_in:
        oauth.login_button("Log in with Google")
        st.stop()
    else:
        user_info = oauth.user_info
        user_email = user_info["email"]
        if users_collection.count_documents({"email": user_email}) == 0:
            users_collection.insert_one({"email": user_email})
        st.success(f"Welcome {user_info['name']}")

    st.markdown(
        """
        <style>
        .st-emotion-cache-q3uqly.ef3psqc13 {
            display: block;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    st.subheader("Click the button below to predict your college!")
    st.divider()
    if st.button("Next", key="next_button", type='primary'):
        st.session_state.page = "main_project"
        st.experimental_rerun()
    st.divider()
    st.write(
        """
        Students often find it difficult to find colleges after their entrance exams, due to various factors.
        To overcome this issue we made SeatAlgo which helps students to find the colleges and branches they were unaware of.
        Potentially making students get better colleges.
        """
    )
    st.divider()

# Define main project page
def main_project():
    st.markdown(
        """
        <style>
        .st-emotion-cache-1v0mbdj.e115fcil1 {
            display: block;
            margin: 0 auto;
        }
        p {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image("seatalgo.png", width=300)
    df = pd.read_csv('final_df2.csv')
    institute_names = pd.read_csv('institute codes.csv')
    institute_mapping = institute_names.set_index('code')['name'].to_dict()
    df['Institute Name'] = df['institute_code'].map(institute_mapping)

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
            key="category_percentile",
            placeholder="Select Category",
        )
        st.write("You selected:", category)
        branch = st.multiselect(
            "Enter your preferred branch",
            np.sort(df['branch_name'].unique()),
            max_selections=5,
            key="branch_percentile"
        )
        if st.button("Submit", key="submit_percentile", type="primary"):
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
            key="category_merit",
            placeholder="Select Category",
        )
        st.write("You selected:", category)
        branch = st.multiselect(
            "Enter your preferred branch",
            np.sort(df['branch_name'].unique()),
            max_selections=5,
            key="branch_merit"
        )
        if st.button("Submit", key="submit_merit", type="primary"):
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
