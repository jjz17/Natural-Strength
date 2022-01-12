import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports
from multipage import MultiPage
from pages import example, records, user_dashboard # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
# display = Image.open('Logo.png')
# display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
# col1, col2 = st.beta_columns(2)
# col1.image(display, width = 400)
# col2.title("Data Storyteller Application")

# Add all your application here
# app.add_page('Upload Data', records.app)
app.add_page('USAPL American Records', records.app)
app.add_page('Personal Dashboard', user_dashboard.app)

# The main app
app.run()