import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv('final_df2.csv')
institute_names = pd.read_csv('institute codes.csv')

# Map institute codes to names
institute_mapping = institute_names.set_index('code')['name'].to_dict()
df['Institute Name'] = df['institute_code'].map(institute_mapping)

# Page title
st.title("College Admission Predictor")

# Sidebar option for input method
input_option = st.sidebar.radio("Choose Input Method", ("MHT-CET Percentile", "MHT-CET Merit No."))

# Data preprocessing
le = LabelEncoder()
df['Category'] = le.fit_transform(df['Category'])
df['branch_name'] = le.fit_transform(df['branch_name'])
X = df[['MHT-CET Score', 'Category', 'branch_name']].values
y = df['Institute Name'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
ada_clf = AdaBoostClassifier(n_estimators=100, random_state=42)
ada_clf.fit(X_train, y_train)

# Input fields based on user choice
if input_option == "MHT-CET Percentile":
    percentile = st.sidebar.number_input("Enter MHT-CET Percentile", value=None, step=0.01)
    Merit = None
else:
    Merit = st.sidebar.number_input("Enter MHT-CET Merit No.", value=None)

# Check if both inputs are provided
if percentile is not None and Merit is not None:
    st.error("Please provide only one input (Percentile or Merit No.)")

# Prediction based on user input
if percentile is not None:
    category = st.selectbox("Select Category: ", df['Category'].unique(), index=None)
    branch = st.multiselect("Select Preferred Branches: ", np.sort(df['branch_name'].unique()), max_selections=5)
    if st.button("Predict College", type="primary"):
        input_data = np.array([[percentile, le.transform([category])[0], le.transform(branch)]])
        college_prediction = ada_clf.predict(input_data)
        st.success("Predicted College:")
        st.write(college_prediction[0])
elif Merit is not None:
    category = st.selectbox("Select Category: ", df['Category'].unique(), index=None)
    branch = st.multiselect("Select Preferred Branches: ", np.sort(df['branch_name'].unique()), max_selections=5)
    if st.button("Predict College", type="primary"):
        input_data = np.array([[Merit, le.transform([category])[0], le.transform(branch)]])
        college_prediction = ada_clf.predict(input_data)
        st.success("Predicted College:")
        st.write(college_prediction[0])
else:
    st.warning("Please provide either MHT-CET percentile or Merit No.")
