import streamlit as st
import pandas as pd
from data_handler import DataHandler

def _filters(df: pd.DataFrame):
    col1, col2, col3 = st.columns(3)
    with col1:
        by_client = st.selectbox("Client", options=["All"] + sorted(df['client'].dropna().unique().tolist()) if len(df) else ["All"])
    with col2:
        by_status = st.selectbox("Status", options=["All"] + sorted(df['status'].dropna().unique().tolist()) if len(df) else ["All"])
    with col3:
        search = st.text_input("Search by Name/Position")
    filtered = df.copy()
    if len(filtered):
        if by_client != "All":
            filtered = filtered[filtered['client'] == by_client]
        if by_status != "All":
            filtered = filtered[filtered['status'] == by_status]
        if search:
            mask = filtered['name'].str.contains(search, case=False, na=False) | filtered['position'].str.contains(search, case=False, na=False)
            filtered = filtered[mask]
    return filtered

def _new_candidate_form(dh: DataHandler):
    st.subheader("Add Candidate")
    with st.form("add_candidate_form", clear_on_submit=True):
        name = st.text_input("Name", "")
        position = st.text_input("Position", "")
        status = st.selectbox("Status", ["Open", "In Progress", "Interview", "Hired", "Rejected"])
        client = st.text_input("Client", "")
        applied_date = st.date_input("Applied Date")
        submitted = st.form_submit_button("Add")
        if submitted:
            if not name or not position:
                st.warning("Name and Position are required.")
            else:
                cid = dh.add_candidate({
                    "name": name,
                    "position": position,
                    "status": status,
                    "client": client,
                    "applied_date": applied_date
                })
                st.success(f"Candidate added with ID {cid}")

def _edit_delete_section(dh: DataHandler, df: pd.DataFrame):
    st.subheader("Edit / Delete")
    if len(df) == 0:
        st.info("No candidates to edit.")
        return
    selected_id = st.selectbox("Select Candidate ID", options=df['id'].tolist())
    selected_row = df[df['id'] == selected_id].iloc[0]
    with st.form("edit_candidate_form"):
        name = st.text_input("Name", selected_row['name'])
        position = st.text_input("Position", selected_row['position'])
        status = st.selectbox("Status", ["Open", "In Progress", "Interview", "Hired", "Rejected"], index=["Open", "In Progress", "Interview", "Hired", "Rejected"].index(selected_row['status']) if selected_row['status'] in ["Open", "In Progress", "Interview", "Hired", "Rejected"] else 0)
        client = st.text_input("Client", selected_row['client'])
        applied_date = st.date_input("Applied Date", selected_row['applied_date'])
        c1, c2 = st.columns(2)
        with c1:
            update = st.form_submit_button("Update")
        with c2:
            delete = st.form_submit_button("Delete")
    if update:
        ok = dh.update_candidate(int(selected_id), {
            "name": name,
            "position": position,
            "status": status,
            "client": client,
            "applied_date": applied_date
        })
        if ok:
            st.success("Candidate updated.")
        else:
            st.error("Update failed.")
    if delete:
        # Simple delete by overwriting file without the row
        all_df = dh.load_candidates()
        all_df = all_df[all_df['id'] != int(selected_id)]
        all_df.to_excel(dh.candidates_file, index=False)
        st.success("Candidate deleted.")

def _upload_excel(dh: DataHandler):
    st.subheader("Upload Candidates Excel")
    up = st.file_uploader("Upload .xlsx", type=["xlsx"])
    if up:
        try:
            df = pd.read_excel(up)
            # Store to "database" placeholder (Excel)
            dh.save_candidates(df)
            st.success("Candidates uploaded and saved.")
        except Exception as e:
            st.error(f"Upload failed: {e}")

# PUBLIC_INTERFACE
def render_candidates_page():
    """Render the Candidates page with CRUD, filtering, and upload support."""
    st.title("Candidates")
    dh = DataHandler(data_dir="data")
    df = dh.load_candidates()

    _upload_excel(dh)

    st.subheader("Candidates List")
    filtered = _filters(df) if len(df) else df
    st.dataframe(filtered, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        _new_candidate_form(dh)
    with col2:
        _edit_delete_section(dh, df)

render_candidates_page()
