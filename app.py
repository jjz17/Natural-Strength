# Custom imports
import streamlit as st
from src.multipage import MultiPage
from pages import records, user_dashboard, data_insights, resources, about  # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
# display = Image.open('Logo.png')
# display = np.array(display)
# st.image(display, width = 400)
st.title('Natural Strength Building')
st.text('Progress with Real Raw Data')
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
# col1, col2 = st.beta_columns(2)
# col1.image(display, width = 400)
# col2.title("Data Storyteller Application")

# Add all your application here
# app.add_page('Upload Data', records.app)
app.add_page('USAPL American Records', records.app)
app.add_page('Personal Dashboard', user_dashboard.app)
app.add_page('Model Data Visualizations', data_insights.app)
app.add_page('Resources', resources.app)
app.add_page('About Us', about.app)

# The main app
app.run()