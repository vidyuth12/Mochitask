"""
import streamlit as st
from gsheet_utils import log_mood, get_mood_data
from mood_constants import MOOD_EMOJIS
from datetime import datetime
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Mood Logger", page_icon="📝", layout="centered")

st.title("📝 Mood Logger")

# Mood Input
st.subheader("How are you feeling?")
mood = st.selectbox("Select a mood", options=list(MOOD_EMOJIS.keys()), format_func=lambda x: f"{MOOD_EMOJIS[x]} {x}")
note = st.text_input("Add a note (optional)")
if st.button("Log Mood"):
    log_mood(mood, note)
    st.success("Mood logged!")

st.divider()

# Visualization
st.subheader("📊 Mood Summary for Today")

df = get_mood_data()
if not df.empty:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    today = datetime.now().date()
    today_df = df[df['Timestamp'].dt.date == today]

    if not today_df.empty:
        mood_counts = today_df['Mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']
        fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood',
                     title="Mood Counts Today", text='Count')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No moods logged today yet.")
else:
    st.info("No mood data available yet.")
"""
import streamlit as st
from datetime import datetime, date
import pandas as pd
import time
from gsheet_utils import log_mood, get_mood_data
import plotly.express as px

st.set_page_config(page_title="Mood Tracker 😊", layout="centered")

st.title("🧠 Mood Logger")
st.markdown("Log your mood and visualize how your day is going!")

# --- Mood Emoji Buttons ---
mood_options = {
    "😊": "Happy",
    "😠": "Angry",
    "😕": "Confused",
    "🎉": "Excited",
    "😢": "Sad"
}

st.subheader("How are you feeling?")
cols = st.columns(len(mood_options))

selected_mood = None
for i, (emoji, label) in enumerate(mood_options.items()):
    if cols[i].button(f"{emoji} {label}"):
        selected_mood = label
        st.toast(f"Mood logged: {emoji} {label}")

note = st.text_input("Optional Note", placeholder="e.g. 'Long meetings today...'")

if selected_mood:
    log_mood(selected_mood, note)
    st.rerun()  # Refresh after logging mood

# --- Mood History & Filter ---
st.divider()
st.subheader("📊 Mood Chart")

# Filter by date
df = get_mood_data()
if df.empty:
    st.info("No mood entries yet.")
    st.stop()

# Ensure Timestamp column is datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

filter_date = st.date_input("Filter by date", value=date.today())
filtered_df = df[df['Timestamp'].dt.date == filter_date]

if filtered_df.empty:
    st.warning("No moods logged for this date.")
else:
    mood_counts = filtered_df['Mood'].value_counts().reset_index()
    mood_counts.columns = ['Mood', 'Count']

    fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood',
                 title=f"Mood Count for {filter_date.strftime('%B %d, %Y')}",
                 height=400)

    st.plotly_chart(fig, use_container_width=True)

# --- Auto-refresh Button ---
st.button("🔁 Refresh Chart", on_click=st.rerun)
