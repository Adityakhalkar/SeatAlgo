# contents to be added here
import streamlit as st
import pandas as pd
df = pd.read_csv('final_df2.csv')
st.title("Seat Algo")

percentile = st.number_input("MHT-CET Percentile", value=None, placeholder="Enter your MHT-CET percentile")
Merit = st.number_input("MHT-CET Merit No.", value=None, placeholder="Enter your Merit Number")
category = st.selectbox(
    "Select your Category: ",
    df['Category'].unique(),
    index=None,
    placeholder="Select Category",
)
st.write("You selected:", category)
branch = st.multiselect(
    "Enter your preferred branch",
    df['branch_name'].unique(),
    max_selections = 5
)
@st.cache_data
def load_data(colleges):
    return pd.DataFrame(
        {
            "Allotable Institutes": colleges,
        }
    )
if st.button("Submit", type = "primary"):
    colleges = df['institute_code'][(df['Merit No.'] < Merit) & (df['MHT-CET Score'] > percentile) & (df['Category'] == category)].unique()
    data_df = load_data(colleges)

    st.data_editor(
        data_df,
        column_config={
            "Allotable Colleges": st.column_config.TextColumn(
                "Allotable Colleges",
                help="Streamlit **widget** commands 🎈",
                default="st.",
                max_chars=50,
                validate="^st\.[a-z_]+$",
            )
        },
        hide_index=True,
    )