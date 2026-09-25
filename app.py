# pyright: reportMissingImports=false
# pyright: reportMissingModuleSource=false
import streamlit as st  # type: ignore[import-not-found]
import pandas as pd  # type: ignore[import-not-found]
import datetime
import os

try:
    import plotly.express as px  # type: ignore[import-not-found]
except ImportError:
    px = None

if px is None:
    st.warning("Plotly is not installed; chart visualizations will be disabled.")

# --- Streamlit App Structure (Rewriting ipywidgets functionality) ---

st.set_page_config(layout="wide", page_title="BJJ Master Tracker")

st.title("🥋 BJJ Master Training & Study App")
st.markdown("--- Streamlit Version ---")

# NOTE: This is a starting point. The full ipywidgets application logic
# needs to be reimplemented here using Streamlit's components.

# Ensure data directory exists and initialize files
DATA_DIR = "bjj_master_data"
LOGFILE = os.path.join(DATA_DIR, "training_logs.csv")
STUDYFILE = os.path.join(DATA_DIR, "study_banks.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize Training Log CSV if it doesn't exist
if not os.path.exists(LOGFILE):
    df_log_init = pd.DataFrame(columns=["Date", "Rank", "Stripes", "Style",
                                         "Duration", "Rounds", "Techniques_trained",
                                         "Submissions_Given", "Submissions_Received", "Notes"])
    df_log_init.to_csv(LOGFILE, index=False)

# Initialize Technique Study Bank if it doesn't exist
if not os.path.exists(STUDYFILE):
    initial_studies = [
        {
            "Title": "Guillotine to Clamp Guard Reaction Chain",
            "Category": "Guard / Closed Guard",
            "Athlete_Source": "Brianna Ste-Marie vs Morgan Black (No-Gi Worlds 2024)",
            "Video_URL": "https://www.youtube.com/watch?v=BzwFZSrxJkM",
            "Key_Details": "Use head post in clinch to disrupt posture and neutralize takedown. On single-leg shot, catch neck immediately into high-elbow guillotine. Jump to clamp guard (body triangle/high guard) to eliminate posture and prevent walking out."
        },
        {
            "Title": "Guard Pull to Pendulum & Lumberjack Sweep",
            "Category": "Guard / Closed Guard",
            "Athlete_Source": "Helena Crevar vs Gabriela Miranda (No-Gi Worlds 2025)",
            "Video_URL": "https://www.youtube.com/watch?v=IGaL1pyNtuU",
            "Key_Details": "Hand-to-hand grip pull to closed guard. Use feet-on-shoulders as defensive frame when top player stands. Failed pendulum sweep transitions into hip heist or guillotine. If opponent stands to defend guillotine, finish with Lumberjack Sweep loading hips onto theirs."
        },
        {
            "Title": "Kimura Reaction Decision Tree (Armbar / Triangle / Omoplata)",
            "Category": "Guard / Submissions",
            "Athlete_Source": "Adele Fornarino System",
            "Video_URL": "https://www.youtube.com/watch?v=v1wTVPUS4I8",
            "Key_Details": "Push hands off hips -> Kimura grip -> Redirect push-back force into posture break & collar tie. Shrimp & foot on hip for armbar. Branch A: If arm yanks, catch in clamp guard -> Front Triangle. Branch B: If hand ducks under hip, frame head, tricep grip, foot over head -> Hip heist + hip-to-hip whizzer -> Omoplata."
        },
        {
            "Title": "Half Guard Rescue: Knee Lever vs. Windmill Bridge",
            "Category": "Half Guard / Escapes",
            "Athlete_Source": "Sensei Glick & Giancarlo Bodoni",
            "Video_URL": "https://www.youtube.com/watch?v=wg21Vd0Dzz8",
            "Key_Details": "Race condition: Intercept cross-face at source using bicep block. Path A (Knee grounded): Knee-elbow escape x2 -> Clamp. Path B (Knee raised/lever denied): Feet close to buttocks, explosive bridge + windmill arm sweep, block opponent's knee, secure palm-up wrist grip -> Slide knee to hip -> Clamp."
        },
        {
            "Title": "GSP Level-Change Double & Level-Change Single",
            "Category": "Wrestling / Takedowns",
            "Athlete_Source": "Georges St-Pierre (GSP)",
            "Video_URL": "https://www.youtube.com/watch?v=_y7ZXxjJNJw",
            "Key_Details": "1. Keep head posture straight. 2. Shoot elbow-deep hugging back of thighs. 3. Turn the corner with their pressure instead of forcing forward. 4. For single transition: Maintain inside bicep control, pull to make leg light, keep head on shoulder higher than hips, and step forward to collect the secondary leg when defended."
        }
    ]
    pd.DataFrame(initial_studies).to_csv(STUDYFILE, index=False)


# --- 1. Session Logging Tab (Example) ---
st.header("📝 Log Your Training Session")

with st.expander("Log a New Session"): # Using expander for cleaner layout
    
    # Widgets for input
    log_date = st.date_input("Date:", datetime.date.today())
    log_rank_options = ['White', 'Blue', 'Purple', 'Brown', 'Black']
    log_rank = st.selectbox("Rank:", log_rank_options, index=1) # Default to Blue
    log_stripes = st.slider("Stripes:", 0, 4, 0)
    log_style_options = ['Gi', 'No-Gi', 'Both']
    log_style = st.selectbox("Style:", log_style_options)
    log_duration = st.number_input("Duration (hours):", value=1.0, min_value=0.1, step=0.1)
    log_rounds = st.number_input("Rounds:", value=5, min_value=0, step=1)
    log_techniques = st.text_input("Techniques Trained:", placeholder='e.g., Triangle, Armbar')
    log_subs_given = st.number_input("Submissions Given:", value=0, min_value=0, step=1)
    log_subs_received = st.number_input("Submissions Received:", value=0, min_value=0, step=1)
    log_notes = st.text_area("Notes:", placeholder='Any specific insights, challenges, or focus areas...')

    if st.button("Log Session", key="log_session_button"): # Unique key for button
        new_log_entry = {
            "Date": log_date.strftime('%Y-%m-%d'),
            "Rank": log_rank,
            "Stripes": log_stripes,
            "Style": log_style,
            "Duration": log_duration,
            "Rounds": log_rounds,
            "Techniques_trained": log_techniques,
            "Submissions_Given": log_subs_given,
            "Submissions_Received": log_subs_received,
            "Notes": log_notes
        }

        try:
            if os.path.exists(LOGFILE):
                df_log = pd.read_csv(LOGFILE)
                df_log = pd.concat([df_log, pd.DataFrame([new_log_entry])], ignore_index=True)
            else:
                df_log = pd.DataFrame([new_log_entry])
            df_log.to_csv(LOGFILE, index=False)
            st.success("✅ Session logged successfully!")
        except Exception as e:
            st.error(f"Error logging session: {e}")


# --- 2. Study Bank (Placeholder) ---
st.header("📚 Study Bank & Breakdown Library (To be implemented)")
st.info("The study bank functionality from the ipywidgets app would be reimplemented here using Streamlit widgets.")

# --- 3. System Decision Trees (Placeholder) ---
st.header("🌳 System Decision Trees (To be implemented)")
st.info("The static HTML for decision trees would be integrated here, possibly using `st.markdown` with `unsafe_allow_html=True`.")

# --- 4. Analytics Dashboard (Example) ---
st.header("📊 Training Progression Analytics")

if st.button("Refresh Dashboard", key="refresh_dash_button"):  # Using a button for explicit refresh
    if os.path.exists(LOGFILE):
        df = pd.read_csv(LOGFILE)
        if not df.empty:
            df['Date'] = pd.to_datetime(df['Date'])

            total_hours = df["Duration"].sum()
            total_sessions = len(df)
            total_rounds = df["Rounds"].sum()

            st.subheader("Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Hours", f"{total_hours:.1f}")
            col2.metric("Total Sessions", total_sessions)
            col3.metric("Total Rounds", total_rounds)

            if "Date" in df.columns:
                monthly_hours = df.groupby(df["Date"].dt.to_period("M")).agg({"Duration": "sum"}).reset_index()
                monthly_hours["Date"] = monthly_hours["Date"].astype(str)
                st.subheader("Monthly Training Volume")
                if px is not None:
                    fig = px.bar(monthly_hours, x="Date", y="Duration", title="Hours per Month")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write(monthly_hours)

            if "Rank" in df.columns:
                rank_counts = df["Rank"].value_counts()
                st.subheader("Rank Distribution")
                if px is not None:
                    fig2 = px.pie(rank_counts, values=rank_counts.values, names=rank_counts.index, title="Rank Distribution")
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.bar_chart(rank_counts)

            if "Style" in df.columns:
                style_counts = df["Style"].value_counts()
                st.subheader("Style Breakdown")
                if px is not None:
                    fig3 = px.bar(style_counts, x=style_counts.index, y=style_counts.values, title="Style Breakdown")
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.bar_chart(style_counts)

        else:
            st.info("No training logs yet. Log a session to populate the dashboard.")
    else:
        st.info("No training log file found yet.")

# Optional: Show recent logs
st.subheader("Recent Sessions")
if os.path.exists(LOGFILE):
    recent_df = pd.read_csv(LOGFILE)
    if not recent_df.empty:
        st.dataframe(recent_df.tail(10), use_container_width=True)
    else:
        st.info("No sessions logged yet.")
else:
    st.info("No sessions logged yet.")
