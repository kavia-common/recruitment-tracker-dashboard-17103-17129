# Recruitment Dashboard

A Streamlit-based recruitment tracking dashboard with Google OAuth authentication, role-based access control, and interactive visualizations.

## Features

- Google OAuth Authentication
- Role-based access control
- Interactive KPI metrics
- Data visualization using Plotly
- Excel-based data management
- Admin panel for data uploads
- Notification system for open positions

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with the following:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

3. Run the application:
```bash
streamlit run app.py
```

## User Roles

- Admin: Full access, including data management
- Recruiter: Access to candidates and interviews
- Hiring Manager: Access to overview and interviews
- Viewer: Read-only access to overview

## Data Structure

The application uses Excel files for data storage (can be extended to use a database):

- candidates.xlsx: Candidate information
- interviews.xlsx: Interview schedules and feedback
- clients.xlsx: Client company information

## Theme

Uses the Ocean Professional theme with:
- Primary: #2563EB (Blue)
- Secondary: #F59E0B (Amber)
- Modern, clean interface with gradients and subtle shadows
