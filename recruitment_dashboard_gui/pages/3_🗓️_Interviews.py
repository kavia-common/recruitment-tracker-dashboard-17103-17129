import streamlit as st
import pandas as pd
from data_handler import DataHandler

def _filters(df: pd.DataFrame):
    col1, col2 = st.columns(2)
    with col1:
        by_status = st.selectbox("Status", options=["All"] + sorted(df['status'].dropna().unique().tolist()) if len(df) else ["All"])
    with col2:
        search = st.text_input("Search by Interviewer")
    filtered = df.copy()
    if len(filtered):
        if by_status != "All":
            filtered = filtered[filtered['status'] == by_status]
        if search:
            filtered = filtered[filtered['interviewer'].str.contains(search, case=False, na=False)]
    return filtered

def _new_interview_form(dh: DataHandler):
    st.subheader("Schedule Interview")
    with st.form("add_interview_form", clear_on_submit=True):
        candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
        interviewer = st.text_input("Interviewer", "")
        date = st.date_input("Date")
        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
        feedback = st.text_area("Feedback", "")
        submitted = st.form_submit_button("Schedule")
        if submitted:
            if not interviewer:
                st.warning("Interviewer is required.")
            else:
                iid = dh.add_interview({
                    "candidate_id": int(candidate_id),
                    "interviewer": interviewer,
                    "date": date,
                    "status": status,
                    "feedback": feedback
                })
                st.success(f"Interview scheduled with ID {iid}")

def _update_interview_form(dh: DataHandler, df: pd.DataFrame):
    st.subheader("Update Interview")
    if len(df) == 0:
        st.info("No interviews to update.")
        return
    selected_id = st.selectbox("Select Interview ID", options=df['id'].tolist())
    row = df[df['id'] == selected_id].iloc[0]
    with st.form("edit_interview_form"):
        interviewer = st.text_input("Interviewer", row['interviewer'])
        date = st.date_input("Date", value=row['date'])
        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"], index=["Scheduled", "Completed", "Cancelled"].index(row['status']) if row['status'] in ["Scheduled", "Completed", "Cancelled"] else 0)
        feedback = st.text_area("Feedback", row.get('feedback', ""))
        update = st.form_submit_button("Update")
    if update:
        ok = dh.update_interview(int(selected_id), {
            "interviewer": interviewer,
            "date": date,
            "status": status,
            "feedback": feedback
        })
        if ok:
            st.success("Interview updated.")
        else:
            st.error("Update failed.")

# PUBLIC_INTERFACE
def render_interviews_page():
    """Render the Interviews page with filters and add/edit functionality."""
    st.title("Interviews")
    dh = DataHandler(data_dir="data")
    df = dh.load_interviews()
    st.subheader("Interviews List")
    filtered = _filters(df) if len(df) else df
    st.dataframe(filtered, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        _new_interview_form(dh)
    with col2:
        _update_interview_form(dh, df)

render_interviews_page()
