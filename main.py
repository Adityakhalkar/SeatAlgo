import streamlit as st

st.image("seatalgo.png", use_column_width=True)
# Description of the project
    
st.write("""

        
        Guess no more, which college you will get is predicted by our model. 
        Check your Seat allocation status right now by clicking the below button.
""")
# Center align the button
if st.button("Next"):
    st.button.page_link("pages/app.py", label="Next")


