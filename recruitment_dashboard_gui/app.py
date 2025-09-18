import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PUBLIC_INTERFACE
def init_theme():
    """Apply page config and custom CSS for Ocean Professional theme."""
    st.set_page_config(
        page_title="Recruitment Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
        :root {
            --primary: #2563EB;
            --secondary: #F59E0B;
            --bg: #f9fafb;
            --surface: #ffffff;
            --text: #111827;
        }
        .main { background-color: var(--bg); }
        .stButton button {
            background: linear-gradient(90deg, #2563EB, #1d4ed8);
            color: white; border: 0; border-radius: 8px; padding: 0.5rem 1rem;
            box-shadow: 0 2px 8px rgba(37,99,235,0.25);
        }
        .stMetric { background: #fff; padding: 1rem; border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
        .notification-banner {
            padding: 1rem;
            background: linear-gradient(90deg, rgba(37,99,235,0.08), rgba(249,250,251,1));
            border-radius: 10px; margin-bottom: 1rem;
            border: 1px solid rgba(37,99,235,0.15);
        }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# PUBLIC_INTERFACE
def render_home():
    """Render the home landing for the Streamlit multi-page app."""
    init_theme()
    st.title("Recruitment Tracker Dashboard")
    st.write("Use the left Pages menu to navigate: Overview, Candidates, Interviews, Clients, Actions.")
    st.info("Tip: Upload Excel files in respective pages to update data. Snowflake integration hooks are prepared for future steps.")

if __name__ == "__main__":
    render_home()
