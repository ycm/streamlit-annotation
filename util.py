import constants
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path


def get_xray_array(path):
    return np.random.randint(0, 256, size=(2048, 2048))


def get_xray_paths_for_user(username):
    return [
        "k4z1m2qa",
        "b8t0xqpl",
        "n3y7sd2a",
        "c6jv1k9z",
        "x2q8lm4n",
        "p0t9s6df",
        "w3r5ab7k",
        "z8n1q4cd",
        "h6v2m0xp",
        "t9y3sk1b",
    ]


def authenticate(username, password):
    return username in st.secrets.users and st.secrets.users[username] == password


def get_annotations_filename_for_user(username):
    return Path(f"{username}_annotations.parquet")


def load_annotations_for_user(username):
    f = get_annotations_filename(username)
    if f.exists():
        return pd.read_parquet(f)
    return pd.DataFrame()


def save_annotations(df, username):
    df.to_parquet(get_annotations_filename_for_user(username), index=False)


def record_annotation(df, username, path, answers):
    row = {"path": path}
    row.update(answers)

    df = df[df["path"] != path] if "path" in df else df
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    save_annotations(df, username)

    return df


def is_finished(row):
    for q in constants.QUESTIONS:
        if row.get(q) is None:
            return False
    return True


def find_first_unfinished(paths, df):
    if df.empty:
        return 0

    answered = {r["path"]: r for _, r in df.iterrows()}

    for i, p in enumerate(paths):
        if p not in answered:
            return i

        if not is_finished(answered[p]):
            return i

    return 0
