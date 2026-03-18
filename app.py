import streamlit as st

from pages.login import login_page
from pages.annotate import annotation_page

# wide layout
st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    annotation_page()
