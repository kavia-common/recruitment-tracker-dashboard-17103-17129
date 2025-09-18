import streamlit as st
from visualizations import DashboardVisualizations
from data_handler import DataHandler

# PUBLIC_INTERFACE
def render_overview_page():
    """Render the Overview page showing KPIs and summary charts."""
    st.title("Dashboard Overview")

    dh = DataHandler(data_dir="data")
    data = dh.load_all_data()

    # KPI Metrics
    metrics = dh.get_recruitment_metrics()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Candidates", metrics['total_candidates'], delta=metrics['recent_candidates'])
    with c2:
        st.metric("Open Positions", metrics['open_positions'])
    with c3:
        st.metric("Active Interviews", metrics['active_interviews'])
    with c4:
        st.metric("Success Rate", f"{metrics['success_rate']:.1f}%")

    # Notifications
    with st.container():
        try:
            candidates_df = data['candidates']
            open_positions = candidates_df[candidates_df['status'] == 'Open']['position'].unique()
            if len(open_positions) > 0:
                st.info(f"📢 Currently {len(open_positions)} open positions: {', '.join(open_positions)}")
        except Exception:
            pass

    # Filters
    st.subheader("Filters")
    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        client_filter = st.selectbox("Filter by Client", options=["All"] + sorted([c for c in data['candidates']['client'].dropna().unique()]) if len(data['candidates']) else ["All"])
    with colf2:
        status_filter = st.selectbox("Filter by Status", options=["All"] + sorted([s for s in data['candidates']['status'].dropna().unique()]) if len(data['candidates']) else ["All"])
    with colf3:
        position_filter = st.selectbox("Filter by Position", options=["All"] + sorted([p for p in data['candidates']['position'].dropna().unique()]) if len(data['candidates']) else ["All"])

    candidates_df = data['candidates'].copy()
    if len(candidates_df):
        if client_filter != "All":
            candidates_df = candidates_df[candidates_df['client'] == client_filter]
        if status_filter != "All":
            candidates_df = candidates_df[candidates_df['status'] == status_filter]
        if position_filter != "All":
            candidates_df = candidates_df[candidates_df['position'] == position_filter]

    viz = DashboardVisualizations(theme_colors={
        "primary": "#2563EB",
        "secondary": "#F59E0B",
        "success": "#F59E0B",
        "error": "#EF4444",
        "text": "#111827"
    })

    col1, col2 = st.columns(2)
    with col1:
        fig_stack = viz.create_candidate_status_chart(candidates_df) if len(candidates_df) else None
        if fig_stack:
            st.plotly_chart(fig_stack, use_container_width=True)
        else:
            st.empty()
    with col2:
        fig_pie = viz.create_position_distribution_chart(candidates_df) if len(candidates_df) else None
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.empty()

    st.subheader("Interview Timeline")
    fig_timeline = viz.create_interview_timeline(data['interviews'])
    if fig_timeline:
        st.plotly_chart(fig_timeline, use_container_width=True)

# Auto-run when executed as a Streamlit page
render_overview_page()
