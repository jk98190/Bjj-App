# -*- coding: utf-8 -*-

import os
import datetime as dt
import pandas as pd
import streamlit as st

# -----------------------------
# Configuration
# -----------------------------
LOGFILE = "training_log.csv"

COLUMNS = [
    "Date",
    "Rank",
    "Stripes",
    "Style",
    "Duration",
    "Rounds",
    "Techniques_trained",
    "Submissions_Given",
    "Submissions_Received",
    "Notes",
]


def logs():
    """Load the training log, creating it if it does not exist."""
    if os.path.exists(LOGFILE):
        try:
            df = pd.read_csv(LOGFILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            df = pd.DataFrame(columns=COLUMNS)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    # Make sure all expected columns exist.
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[COLUMNS]


def log_training():
    st.title("📝 Log Training")
    st.caption(
        "Record a training session using the same fields as the original notebook."
    )

    with st.form("log"):
        a, b, c = st.columns(3)

        date = a.date_input("Date", dt.date.today())

        rank = b.selectbox(
            "Rank",
            ["White", "Blue", "Purple", "Brown", "Black"],
            index=1,
        )

        stripes = c.slider("Stripes", 0, 4, 0)

        a, b, c = st.columns(3)

        style = a.selectbox("Style", ["Gi", "No-Gi", "Both"])

        duration = b.number_input(
            "Duration (hours)",
            min_value=0.1,
            value=1.0,
            step=0.1,
        )

        rounds = c.number_input(
            "Rounds",
            min_value=0,
            value=5,
            step=1,
        )

        tech = st.text_input(
            "Techniques Trained",
            placeholder="Triangle, Armbar",
        )

        a, b = st.columns(2)

        given = a.number_input(
            "Submissions Given",
            min_value=0,
            value=0,
            step=1,
        )

        received = b.number_input(
            "Submissions Received",
            min_value=0,
            value=0,
            step=1,
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Save Training Session",
            type="primary",
        )

        if submitted:
            d = logs()

            row = {
                "Date": date.strftime("%Y-%m-%d"),
                "Rank": rank,
                "Stripes": stripes,
                "Style": style,
                "Duration": duration,
                "Rounds": rounds,
                "Techniques_trained": tech,
                "Submissions_Given": given,
                "Submissions_Received": received,
                "Notes": notes,
            }

            updated = pd.concat(
                [d, pd.DataFrame([row])],
                ignore_index=True,
            )

            updated.to_csv(LOGFILE, index=False)

            st.success("Training session logged.")
            st.rerun()

    st.subheader("Training History")

    history = logs()

    if history.empty:
        st.info("No training sessions have been logged yet.")
    else:
        history["Date"] = pd.to_datetime(history["Date"], errors="coerce")
        history = history.sort_values("Date", ascending=False)
        history["Date"] = history["Date"].dt.strftime("%Y-%m-%d")

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------
# Main app
# -----------------------------
st.set_page_config(
    page_title="BJJ Training Tracker",
    page_icon="🥋",
    layout="wide",
)

log_training()
