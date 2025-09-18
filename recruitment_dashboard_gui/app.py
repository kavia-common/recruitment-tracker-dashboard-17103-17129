import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Recruitment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme colors from Ocean Professional theme
THEME = {
    "primary": "#2563EB",
    "secondary": "#F59E0B",
    "success": "#F59E0B",
    "error": "#EF4444",
    "background": "#f9fafb",
    "surface": "#ffffff",
    "text": "#111827"
}

# Apply custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f9fafb;
    }
    .stButton button {
        background-color: #2563EB;
        color: white;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .notification-banner {
        padding: 1rem;
        background: linear-gradient(to right, rgba(37,99,235,0.1), rgba(249,250,251,1));
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Role definitions
ROLES = {
    "admin@company.com": "admin",
    "recruiter@company.com": "recruiter",
    "hiring_manager@company.com": "hiring_manager"
}

def load_data():
    """Load data from Excel files (stub for future database integration)"""
    data_path = Path("data")
    if not data_path.exists():
        data_path.mkdir()
        
    # Default empty DataFrames
    if not (data_path / "candidates.xlsx").exists():
        pd.DataFrame({
            "id": [],
            "name": [],
            "position": [],
            "status": [],
            "client": [],
            "applied_date": []
        }).to_excel(data_path / "candidates.xlsx", index=False)
        
    return {
        "candidates": pd.read_excel(data_path / "candidates.xlsx"),
        "interviews": pd.read_excel(data_path / "interviews.xlsx") if (data_path / "interviews.xlsx").exists() else pd.DataFrame(),
        "clients": pd.read_excel(data_path / "clients.xlsx") if (data_path / "clients.xlsx").exists() else pd.DataFrame()
    }

def authenticate():
    """Google OAuth authentication"""
    # Placeholder for Google OAuth implementation
    # In production, implement proper Google OAuth flow
    if st.sidebar.text_input("Email"):
        st.session_state.authenticated = True
        st.session_state.user_email = st.sidebar.text_input("Email")
        st.session_state.user_role = ROLES.get(st.session_state.user_email, "viewer")
        return True
    return False

def show_notifications():
    """Display notification banners for open positions"""
    if st.session_state.get('data', {}).get('candidates') is not None:
        open_positions = st.session_state.data['candidates'][
            st.session_state.data['candidates']['status'] == 'Open'
        ]['position'].unique()
        
        if len(open_positions) > 0:
            with st.container():
                st.markdown(f"""
                <div class="notification-banner">
                    📢 Currently {len(open_positions)} open positions: {', '.join(open_positions)}
                </div>
                """, unsafe_allow_html=True)

def show_metrics():
    """Display KPI metrics"""
    if 'data' not in st.session_state:
        return
    
    candidates_df = st.session_state.data['candidates']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", 
                 len(candidates_df),
                 delta=len(candidates_df[candidates_df['applied_date'] > 
                                      (datetime.now() - pd.Timedelta(days=30))]))
    
    with col2:
        st.metric("Open Positions",
                 len(candidates_df[candidates_df['status'] == 'Open']['position'].unique()))
    
    with col3:
        st.metric("Active Interviews",
                 len(st.session_state.data['interviews'][
                     st.session_state.data['interviews']['status'] == 'Scheduled']))
    
    with col4:
        st.metric("Success Rate",
                 f"{(len(candidates_df[candidates_df['status'] == 'Hired']) / len(candidates_df) * 100):.1f}%")

def show_charts():
    """Display Plotly charts"""
    if 'data' not in st.session_state:
        return
    
    candidates_df = st.session_state.data['candidates']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stacked bar chart - Candidates by status per client
        fig_stack = px.bar(
            candidates_df.groupby(['client', 'status']).size().reset_index(name='count'),
            x='client',
            y='count',
            color='status',
            title='Candidates by Status per Client',
            template='plotly_white'
        )
        st.plotly_chart(fig_stack, use_container_width=True)
    
    with col2:
        # Pie chart - Position distribution
        fig_pie = px.pie(
            candidates_df['position'].value_counts().reset_index(),
            values='count',
            names='position',
            title='Position Distribution',
            template='plotly_white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def admin_panel():
    """Admin-only panel for data management"""
    if st.session_state.user_role != 'admin':
        st.warning("Access denied. Admin privileges required.")
        return
    
    st.subheader("Data Management")
    
    uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.to_excel(f"data/{uploaded_file.name}", index=False)
            st.success("File uploaded successfully!")
            st.session_state.data = load_data()
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")

def main():
    """Main application flow"""
    if not st.session_state.authenticated:
        if not authenticate():
            st.title("Recruitment Dashboard")
            st.write("Please log in to continue")
            return
    
    # Load data
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            "Dashboard",
            ["Overview", "Candidates", "Interviews", "Clients", "Admin"],
            icons=['house', 'person', 'calendar', 'building', 'gear'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fff"},
                "icon": {"color": THEME["primary"], "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px",
                            "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": THEME["primary"]},
            }
        )
    
    # Show notifications
    show_notifications()
    
    if selected == "Overview":
        st.title("Dashboard Overview")
        show_metrics()
        show_charts()
    
    elif selected == "Admin":
        st.title("Admin Panel")
        admin_panel()
    
    # Additional pages to be implemented based on selection
    else:
        st.title(f"{selected}")
        st.write(f"{selected} page under construction")

if __name__ == "__main__":
    main()
