import streamlit as st
import util


def login_page():
    """
    Defines
    """
    _, col_login, _ = st.columns([1, 1, 1])

    with col_login:
        st.subheader("ARDS-QUEST annotator login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if util.authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                paths = util.get_xray_paths_for_user(username)
                df = util.load_annotations_for_user(username)

                st.session_state.paths = paths
                st.session_state.annotations = df
                st.session_state.idx = util.find_first_unfinished(paths, df)
                st.session_state.idx_cache = None
                st.session_state.img = None

                st.rerun()

            else:
                st.error("Invalid username or password")
