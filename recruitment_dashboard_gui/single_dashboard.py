import streamlit as st
from datetime import datetime

# PUBLIC_INTERFACE
def init_theme():
    """Apply page config and inject Ocean Professional modern CSS for consistent styling."""
    st.set_page_config(
        page_title="Recruitment Tracker Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
        :root {
            --primary: #2563EB;      /* Blue */
            --secondary: #F59E0B;    /* Amber */
            --success: #F59E0B;      /* Reusing amber as success accent per guide */
            --error: #EF4444;
            --bg: #f9fafb;
            --surface: #ffffff;
            --text: #111827;
            --shadow-rgb: 37, 99, 235;
        }
        .main { background-color: var(--bg); }
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

        /* Header card */
        .header-card {
            background: linear-gradient(90deg, rgba(37,99,235,0.06), rgba(249,250,251,1));
            border: 1px solid rgba(37,99,235,0.15);
            border-radius: 14px;
            padding: 1rem 1.25rem;
            box-shadow: 0 6px 24px rgba(0,0,0,0.05);
        }

        /* KPI grid: keep cards consistent sizes */
        .kpi-card {
            background: var(--surface);
            border-radius: 14px;
            padding: 1rem 1.25rem;
            box-shadow: 0 6px 24px rgba(0,0,0,0.06);
            border: 1px solid #e5e7eb;
        }
        /* Make st.metric display in our card block look neat */
        div[data-testid="stMetric"] {
            background: transparent !important;
            padding: 0 !important;
        }
        div[data-testid="stMetricValue"] > div {
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] > div {
            color: #6b7280;
            font-weight: 600;
        }

        /* Panel/section card */
        .panel {
            background: var(--surface);
            border-radius: 14px;
            padding: 1rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 6px 24px rgba(0,0,0,0.06);
            height: 100%;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #2563EB, #1d4ed8);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            box-shadow: 0 8px 20px rgba(var(--shadow-rgb), 0.25);
        }
        .stButton > button:hover {
            filter: brightness(1.05);
            transform: translateY(-1px);
        }

        /* Tabs accent */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
            border-bottom: 1px solid #e5e7eb;
        }
        .stTabs [data-baseweb="tab"] {
            background: #f3f4f6;
            color: var(--text);
            border-radius: 10px 10px 0 0;
            padding-top: 0.6rem;
            padding-bottom: 0.6rem;
        }
        .stTabs [aria-selected="true"] {
            background: #ffffff !important;
            border: 1px solid #e5e7eb;
            border-bottom-color: #ffffff;
            color: var(--text);
        }

        /* Inputs focus ring */
        .stSelectbox, .stTextInput, .stDateInput, .stNumberInput, .stTextArea {
            outline: none !important;
        }
        .stSelectbox:focus-within, .stTextInput:focus-within, .stDateInput:focus-within, .stNumberInput:focus-within, .stTextArea:focus-within {
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25);
            border-radius: 8px;
        }

        /* Subtle captions */
        .caption-muted {
            color: #6b7280;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

# PUBLIC_INTERFACE
def render_header():
    """Render the header bar with title and lightweight global controls."""
    with st.container():
        st.markdown('<div class="header-card">', unsafe_allow_html=True)
        left, right = st.columns([0.65, 0.35])
        with left:
            st.markdown("### 📊 Recruitment Tracker Dashboard")
            st.caption("Modern, minimalist layout with Ocean Professional styling.")
        with right:
            c1, c2 = st.columns(2)
            with c1:
                st.date_input("Date Range", value=[datetime.now().replace(month=1, day=1), datetime.now()])
            with c2:
                st.selectbox("Department", options=["All", "Engineering", "Product", "Design", "Sales"], index=0)
            st.caption("Filters are placeholders; no data wiring yet.")
        st.markdown('</div>', unsafe_allow_html=True)

# PUBLIC_INTERFACE
def render_kpis():
    """Render top KPI section with four metrics."""
    st.write("")  # spacing
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Total Applicants", 128, delta="+12 this week")
        st.markdown('</div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Selected", 38, delta="+5")
        st.markdown('</div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Rejected", 54, delta="-2")
        st.markdown('</div>', unsafe_allow_html=True)
    with k4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Selection/Rejected Rate", "41% / 59%", delta="↑ +3%")
        st.markdown('</div>', unsafe_allow_html=True)

# PUBLIC_INTERFACE
def render_placeholder_charts():
    """Render placeholder regions for future charts using responsive columns."""
    st.write("")  # spacing
    st.subheader("Overview Charts")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Stacked Bar — Candidates by Status per Client")
        st.caption("Placeholder: A stacked bar chart will appear here.")
        st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Pie — Position Distribution")
        st.caption("Placeholder: A pie chart will appear here.")
        st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Client Breakdown — Key Accounts")
        st.caption("Placeholder: A client breakdown table or small multiples will appear here.")
        st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

# PUBLIC_INTERFACE
def render_tabs():
    """Render tabbed navigation with mock/sample content for Candidate, Interview, Client, Action."""
    st.write("")
    tabs = st.tabs(["👤 Candidate", "🗓️ Interview", "🏢 Client", "✅ Action"])

    with tabs[0]:
        st.subheader("Candidate")
        colA, colB = st.columns([2, 1], gap="large")
        with colA:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Candidate Pipeline (Mock)")
            st.caption("A pipeline or table of candidates by stage will be displayed here.")
            st.write("- Applied: 56")
            st.write("- In Progress: 24")
            st.write("- Interview: 16")
            st.write("- Hired: 8")
            st.markdown('</div>', unsafe_allow_html=True)
        with colB:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Quick Filters (Mock)")
            st.selectbox("Status", options=["All", "Applied", "In Progress", "Interview", "Hired", "Rejected"])
            st.text_input("Search by name or role")
            st.button("Apply Filters")
            st.caption("Filters are not wired to data yet.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("Interview")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Upcoming Interviews (Mock)")
            st.write("• 2025-09-22 — Jane Smith — Product Manager — Panel")
            st.write("• 2025-09-23 — John Doe — Software Engineer — Tech Screen")
            st.write("• 2025-09-24 — Sarah Wilson — UX Designer — Portfolio Review")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Timeline Placeholder")
            st.caption("A scatter/timeline visualization will be added here.")
            st.empty()
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.subheader("Client")
        c1, c2 = st.columns([1.2, 1], gap="large")
        with c1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Active Clients (Mock)")
            st.write("- TechCorp: 3 active positions")
            st.write("- InnovateTech: 2 active positions")
            st.write("- DataCo: 1 active position")
            st.write("- DesignHub: 2 active positions")
            st.write("- CloudTech: 1 active position")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("##### Client Insights")
            st.caption("Placeholder area for client-specific metrics and charts.")
            st.empty()
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.subheader("Action")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("##### Quick Actions (Mock)")
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            if st.button("Export Report"):
                st.info("Export initiated (placeholder).")
        with c2:
            if st.button("Refresh Data"):
                st.success("Data refreshed (placeholder).")
        with c3:
            if st.button("Notify Stakeholders"):
                st.warning("Notifications queued (placeholder).")
        st.caption("These are placeholders. No backend actions are performed.")
        st.markdown('</div>', unsafe_allow_html=True)

# PUBLIC_INTERFACE
def main():
    """Entrypoint for the single-file Streamlit layout preview."""
    init_theme()
    render_header()
    render_kpis()
    render_placeholder_charts()
    render_tabs()

if __name__ == "__main__":
    main()
