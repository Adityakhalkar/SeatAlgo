import streamlit as st
import pandas as pd
import numpy as np

st.image("seatalgo.png", use_column_width=True)
# Description of the project
    
st.write("""

        
        Guess no more, which college you will get is predicted by our model. 
        Check your Seat allocation status right now by clicking the below button.
""")
# Center align the button
if st.button("Next"):
    st.switch_page("app.py")


