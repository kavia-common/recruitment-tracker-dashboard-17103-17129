import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_handler import DataHandler

def _deadlines_section(candidates: pd.DataFrame):
    st.subheader("Upcoming Deadlines")
    # Placeholder: Assuming 'applied_date' + 14 days as follow-up deadline
    if len(candidates) == 0:
        st.info("No candidates data.")
        return
    df = candidates.copy()
    df['applied_date'] = pd.to_datetime(df['applied_date'], errors='coerce')
    df['follow_up_deadline'] = df['applied_date'] + pd.to_timedelta(14, unit="D")
    upcoming = df[(df['follow_up_deadline'] >= datetime.now()) & (df['follow_up_deadline'] <= datetime.now() + timedelta(days=7))]
    if len(upcoming):
        for _, r in upcoming.iterrows():
            st.warning(f"⏰ Follow-up due for {r['name']} ({r['position']}) by {r['follow_up_deadline'].date()} - Client: {r['client']}")
    else:
        st.success("No upcoming deadlines within next 7 days.")

def _automation_hooks():
    st.subheader("Automation Hooks (Placeholders)")
    st.caption("These actions are placeholders for future integrations (e.g., Snowflake, notifications, ATS API).")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Sync to Snowflake"):
            st.info("Snowflake sync initiated (placeholder).")
    with col2:
        if st.button("Send Reminder Emails"):
            st.info("Reminder emails queued (placeholder).")
    with col3:
        if st.button("Export Reports"):
            st.info("Report export generated (placeholder).")

# PUBLIC_INTERFACE
def render_actions_page():
    """Render the Actions page displaying dynamic notifications and automation placeholders."""
    st.title("Actions")
    dh = DataHandler(data_dir="data")
    data = dh.load_all_data()
    _deadlines_section(data['candidates'])
    st.divider()
    _automation_hooks()

render_actions_page()
