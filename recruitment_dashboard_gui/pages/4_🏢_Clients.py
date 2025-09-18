import streamlit as st
import pandas as pd
from data_handler import DataHandler

# PUBLIC_INTERFACE
def render_clients_page():
    """Render the Clients page with list, upload, and basic add/edit."""
    st.title("Clients")
    dh = DataHandler(data_dir="data")
    df = dh.load_clients()

    st.subheader("Upload Clients Excel")
    up = st.file_uploader("Upload .xlsx", type=["xlsx"], key="clients_upload")
    if up:
        try:
            new_df = pd.read_excel(up)
            dh.save_clients(new_df)
            st.success("Clients uploaded and saved.")
            df = new_df
        except Exception as e:
            st.error(f"Upload failed: {e}")

    st.subheader("Clients List")
    if len(df):
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            name_search = st.text_input("Search by Client Name")
        with col2:
            min_positions = st.number_input("Min Active Positions", min_value=0, step=1, value=0)
        filtered = df.copy()
        if name_search:
            filtered = filtered[filtered['name'].str.contains(name_search, case=False, na=False)]
        if 'active_positions' in filtered.columns:
            filtered = filtered[filtered['active_positions'] >= min_positions]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("No clients available. Upload an Excel to get started.")

    st.divider()
    st.subheader("Add / Edit Client")
    with st.form("client_form", clear_on_submit=True):
        name = st.text_input("Name", "")
        industry = st.text_input("Industry", "")
        active_positions = st.number_input("Active Positions", min_value=0, step=1)
        total_hires = st.number_input("Total Hires", min_value=0, step=1)
        submitted = st.form_submit_button("Save")
    if submitted:
        base = dh.load_clients()
        new_id = int(base['id'].max() + 1) if 'id' in base.columns and len(base) else 1
        row = {
            "id": new_id,
            "name": name,
            "industry": industry,
            "active_positions": active_positions,
            "total_hires": total_hires
        }
        base = pd.concat([base, pd.DataFrame([row])], ignore_index=True)
        dh.save_clients(base)
        st.success("Client saved.")

render_clients_page()
