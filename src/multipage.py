# https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030
# CREDITS/REFERENCES


"""
This file is the framework for generating multiple Streamlit applications
through an object oriented framework.
"""

# Import necessary libraries
import streamlit as st

from pages import utils


# Define the multipage class to manage the multiple apps in our program
class MultiPage:
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []

    def add_page(self, title, func) -> None:
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps

            func: Python function to render this page in Streamlit
        """

        self.pages.append({

            "title": title,
            "function": func
        })

    def run(self):
        # Dropdown to select the page to run
        # st.sidebar.subheader('App Navigation')
        page = st.sidebar.selectbox(label='App Navigation',
                                    options=self.pages,
                                    format_func=lambda page: page['title']
                                    )

        st.sidebar.text('Unit Conversion Tool')

        expander1 = st.sidebar.expander('Lbs ➡️ Kg')

        with expander1:
            lbs_to_kg = st.number_input('Lbs to Kg')
            st.text(f'{round(utils.lbs_to_kg(lbs_to_kg), 2)} Kg')

        expander2 = st.sidebar.expander('Kg ➡️ Lbs')

        with expander2:
            kg_to_lbs = st.number_input('Kg to Lbs')
            st.text(f'{round(utils.kg_to_lbs(kg_to_lbs), 2)} Lbs')

        # st.sidebar.write('Unit Conversions')
        #
        # lbs_to_kg = st.sidebar.number_input('Lbs to Kg')
        # st.sidebar.text(f'{round(utils.lbs_to_kg(lbs_to_kg), 2)} Kg')
        #
        # kg_to_lbs = st.sidebar.number_input('Kg to Lbs')
        # st.sidebar.text(f'{round(utils.kg_to_lbs(kg_to_lbs), 2)} Lbs')

        # run the app function
        page['function']()
