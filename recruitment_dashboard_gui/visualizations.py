import plotly.express as px
import plotly.graph_objects as go

class DashboardVisualizations:
    def __init__(self, theme_colors):
        self.theme_colors = theme_colors
        
    def create_candidate_status_chart(self, candidates_df):
        """Create stacked bar chart showing candidate status by client"""
        if len(candidates_df) == 0:
            return None
            
        fig = px.bar(
            candidates_df.groupby(['client', 'status']).size().reset_index(name='count'),
            x='client',
            y='count',
            color='status',
            title='Candidates by Status per Client',
            template='plotly_white',
            color_discrete_sequence=[
                self.theme_colors['primary'],
                self.theme_colors['secondary'],
                self.theme_colors['success'],
                self.theme_colors['error']
            ]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=self.theme_colors['text']
        )
        
        return fig
        
    def create_position_distribution_chart(self, candidates_df):
        """Create pie chart showing distribution of positions"""
        if len(candidates_df) == 0:
            return None
            
        fig = px.pie(
            candidates_df['position'].value_counts().reset_index(),
            values='count',
            names='position',
            title='Position Distribution',
            template='plotly_white',
            color_discrete_sequence=[
                self.theme_colors['primary'],
                self.theme_colors['secondary'],
                self.theme_colors['success'],
                self.theme_colors['error']
            ]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=self.theme_colors['text']
        )
        
        return fig
        
    def create_interview_timeline(self, interviews_df):
        """Create timeline of scheduled interviews"""
        if len(interviews_df) == 0:
            return None
            
        fig = go.Figure()
        
        for status in interviews_df['status'].unique():
            mask = interviews_df['status'] == status
            fig.add_trace(go.Scatter(
                x=interviews_df[mask]['date'],
                y=interviews_df[mask]['interviewer'],
                mode='markers',
                name=status,
                marker=dict(
                    size=12,
                    color=self.theme_colors['primary'] if status == 'Scheduled' 
                          else self.theme_colors['secondary']
                )
            ))
            
        fig.update_layout(
            title='Interview Timeline',
            xaxis_title='Date',
            yaxis_title='Interviewer',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=self.theme_colors['text']
        )
        
        return fig
        
    def create_recruitment_funnel(self, candidates_df):
        """Create recruitment funnel visualization"""
        if len(candidates_df) == 0:
            return None
            
        fig = go.Figure(go.Funnel(
            y=['Applied', 'In Progress', 'Interview', 'Hired'],
            x=[
                len(candidates_df),
                len(candidates_df[candidates_df['status'] == 'In Progress']),
                len(candidates_df[candidates_df['status'] == 'Interview']),
                len(candidates_df[candidates_df['status'] == 'Hired'])
            ],
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(
            title='Recruitment Funnel',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=self.theme_colors['text']
        )
        
        return fig
