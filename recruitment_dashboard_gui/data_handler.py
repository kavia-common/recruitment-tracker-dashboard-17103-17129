import pandas as pd
from pathlib import Path
from datetime import datetime

class DataHandler:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.candidates_file = self.data_dir / "candidates.xlsx"
        self.interviews_file = self.data_dir / "interviews.xlsx"
        self.clients_file = self.data_dir / "clients.xlsx"
        
    def load_all_data(self):
        """Load all data from Excel files"""
        return {
            "candidates": self.load_candidates(),
            "interviews": self.load_interviews(),
            "clients": self.load_clients()
        }
    
    def load_candidates(self):
        """Load candidates data"""
        if self.candidates_file.exists():
            df = pd.read_excel(self.candidates_file)
            df['applied_date'] = pd.to_datetime(df['applied_date'])
            return df
        return pd.DataFrame()
    
    def load_interviews(self):
        """Load interviews data"""
        if self.interviews_file.exists():
            df = pd.read_excel(self.interviews_file)
            df['date'] = pd.to_datetime(df['date'])
            return df
        return pd.DataFrame()
    
    def load_clients(self):
        """Load clients data"""
        if self.clients_file.exists():
            return pd.read_excel(self.clients_file)
        return pd.DataFrame()
    
    def save_candidates(self, df):
        """Save candidates data"""
        df.to_excel(self.candidates_file, index=False)
    
    def save_interviews(self, df):
        """Save interviews data"""
        df.to_excel(self.interviews_file, index=False)
    
    def save_clients(self, df):
        """Save clients data"""
        df.to_excel(self.clients_file, index=False)
    
    def add_candidate(self, candidate_data):
        """Add a new candidate"""
        df = self.load_candidates()
        new_id = len(df) + 1 if len(df) > 0 else 1
        candidate_data['id'] = new_id
        df = pd.concat([df, pd.DataFrame([candidate_data])], ignore_index=True)
        self.save_candidates(df)
        return new_id
    
    def update_candidate(self, candidate_id, updated_data):
        """Update candidate information"""
        df = self.load_candidates()
        idx = df.index[df['id'] == candidate_id].tolist()
        if idx:
            for key, value in updated_data.items():
                df.at[idx[0], key] = value
            self.save_candidates(df)
            return True
        return False
    
    def add_interview(self, interview_data):
        """Schedule a new interview"""
        df = self.load_interviews()
        new_id = len(df) + 1 if len(df) > 0 else 1
        interview_data['id'] = new_id
        df = pd.concat([df, pd.DataFrame([interview_data])], ignore_index=True)
        self.save_interviews(df)
        return new_id
    
    def update_interview(self, interview_id, updated_data):
        """Update interview information"""
        df = self.load_interviews()
        idx = df.index[df['id'] == interview_id].tolist()
        if idx:
            for key, value in updated_data.items():
                df.at[idx[0], key] = value
            self.save_interviews(df)
            return True
        return False
    
    def get_recruitment_metrics(self):
        """Calculate recruitment metrics"""
        candidates_df = self.load_candidates()
        interviews_df = self.load_interviews()
        
        total_candidates = len(candidates_df)
        recent_candidates = len(candidates_df[
            candidates_df['applied_date'] > (datetime.now() - pd.Timedelta(days=30))
        ])
        open_positions = len(candidates_df[candidates_df['status'] == 'Open']['position'].unique())
        active_interviews = len(interviews_df[interviews_df['status'] == 'Scheduled'])
        success_rate = (
            len(candidates_df[candidates_df['status'] == 'Hired']) / total_candidates * 100
            if total_candidates > 0 else 0
        )
        
        return {
            'total_candidates': total_candidates,
            'recent_candidates': recent_candidates,
            'open_positions': open_positions,
            'active_interviews': active_interviews,
            'success_rate': success_rate
        }
