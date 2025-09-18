# Recruitment Tracker Dashboard (Streamlit)

This is a multi-page Streamlit application for tracking recruitment KPIs with modern "Ocean Professional" styling.

Features
- Multi-page: Overview, Candidates, Interviews, Clients, Actions
- KPI metrics using st.metric
- Plotly charts: Stacked bar, pie, interview timeline
- Excel upload per page (placeholder for DB persistence)
- Filters/search for all data views
- CRUD-like add/edit/delete for candidates, interviews, clients (Excel-backed)
- Dynamic notifications for upcoming deadlines
- Community Cloud ready (.streamlit/config.toml, requirements.txt)

Run locally
1. pip install -r requirements.txt
2. streamlit run app.py

Deployment (Streamlit Community Cloud)
- Set the working directory to this folder.
- Ensure the data/ folder exists with .xlsx sample files or upload via UI.

Data persistence
- Current implementation uses Excel files in ./data as a placeholder for a database.
- Snowflake hooks can be added in DataHandler methods for load/save functions.

Env variables (optional)
- Create a .env for future Snowflake/GAuth:
  - SNOWFLAKE_ACCOUNT=
  - SNOWFLAKE_USER=
  - SNOWFLAKE_PASSWORD=
  - GOOGLE_CLIENT_ID=
  - GOOGLE_CLIENT_SECRET=
