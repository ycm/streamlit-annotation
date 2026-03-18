import streamlit as st
import plotly.express as px
import util
import constants


@st.cache_data
def get_xray_fig_from_array(arr):
    fig = px.imshow(arr, color_continuous_scale="gray")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=800)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_coloraxes(showscale=False)

    return fig


def save_answers():
    username = st.session_state.username
    path = st.session_state.paths[st.session_state.idx]
    answers = st.session_state.get("current_answers", {})

    if answers:
        df = st.session_state.annotations
        df = util.record_annotation(
            df,
            username,
            path,
            answers,
        )
        st.session_state.annotations = df


def annotation_page():

    username = st.session_state.username
    paths = st.session_state.paths
    idx = st.session_state.idx

    path = paths[idx]

    col_opts, col_img, col_annotations = st.columns([1, 3, 1], gap="small")

    # ------------------
    # options panel
    # ------------------
    with col_opts:

        st.caption(f"user: {st.session_state.username}")

        nav1, nav2, nav3 = st.columns(3)

        if nav1.button("←"):
            save_answers()
            st.session_state.idx = max(0, idx - 1)
            st.rerun()

        if nav2.button("next unfinished"):
            save_answers()
            st.session_state.idx = util.find_first_unfinished(
                paths, st.session_state.annotations
            )
            st.rerun()

        if nav3.button("→"):
            save_answers()
            st.session_state.idx = min(len(paths) - 1, idx + 1)
            st.rerun()

    # ------------------
    # image panel
    # ------------------
    with col_img:
        if idx != st.session_state.idx_cache:
            st.session_state.img = util.get_xray_array(path)
            st.session_state.idx_cache = idx

        st.plotly_chart(
            get_xray_fig_from_array(st.session_state.img),
            width="stretch",
        )

    # ------------------
    # questions panel
    # ------------------
    with col_annotations:
        answers = {}
        with st.container(height=800):
            for q, opts in constants.QUESTIONS.items():
                answers[q] = st.radio(
                    q,
                    opts,
                    key=f"{path}_{q}",
                    index=None,
                    horizontal=True,
                )
            st.session_state.current_answers = answers

        n_answered = sum(
            1 for _, v in st.session_state.current_answers.items() if v is not None
        )
        st.caption(f"{len(constants.QUESTIONS) - n_answered} questions left")
