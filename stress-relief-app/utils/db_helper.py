"""
Supabase database integration for storing stress data and user information.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional, Dict, List

load_dotenv()


class DBHelper:
    """Handles all Supabase database operations."""
    
    def __init__(self):
        """Initialize the Supabase client."""
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(url, key)
    
    def save_stress_reading(self, user_id: str, stress_level: float, metadata: Optional[Dict] = None) -> bool:
        """
        Save a stress reading to the database.
        
        Args:
            user_id: Unique identifier for the user
            stress_level: Detected stress level (0.0 to 1.0)
            metadata: Optional additional data (eeg_data, timestamp, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'user_id': user_id,
                'stress_level': stress_level,
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': metadata or {}
            }
            
            result = self.supabase.table('stress_readings').insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error saving stress reading: {str(e)}")
            return False
    
    def get_stress_history(self, user_id: str, limit: int = 100) -> List[Dict]:
        """
        Retrieve stress history for a user.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of records to retrieve
            
        Returns:
            List of stress reading dictionaries
        """
        try:
            result = self.supabase.table('stress_readings')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data
        except Exception as e:
            print(f"Error retrieving stress history: {str(e)}")
            return []
    
    def save_intervention_result(self, user_id: str, intervention_type: str, effectiveness: float) -> bool:
        """
        Save the result of a stress relief intervention.
        
        Args:
            user_id: Unique identifier for the user
            intervention_type: Type of intervention used
            effectiveness: Effectiveness rating (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'user_id': user_id,
                'intervention_type': intervention_type,
                'effectiveness': effectiveness,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('interventions').insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error saving intervention result: {str(e)}")
            return False
    
    def save_journal_entry(self, user_id: str, entry_text: str, prompts: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Save a journal entry to the database.
        
        Args:
            user_id: Unique identifier for the user
            entry_text: The journal entry text
            prompts: Optional journal prompts that were used
            metadata: Optional additional data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'user_id': user_id,
                'entry_text': entry_text,
                'prompts': prompts,
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': metadata or {}
            }
            
            result = self.supabase.table('journal_entries').insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error saving journal entry: {str(e)}")
            return False
    
    def get_journal_entries(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Retrieve journal entries for a user.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of entries to retrieve
            
        Returns:
            List of journal entry dictionaries
        """
        try:
            result = self.supabase.table('journal_entries')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data
        except Exception as e:
            print(f"Error retrieving journal entries: {str(e)}")
            return []

