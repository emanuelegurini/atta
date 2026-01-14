from typing import List
import pandas as pd
from atta.core.models import StudentStats
from atta.core.gateway import GSheetGateway

class AttendanceService:
    """
    Service responsible for the business logic:
    - Orchestrating the data fetch.
    - Filtering data for a specific student.
    - Calculating attendance statistics.
    """
    
    def __init__(self, gateway: GSheetGateway = None):
        # We allow dependency injection for testing
        self.gateway = gateway or GSheetGateway()

    def get_stats_for_student(self, student_id: str, sheet_url: str) -> StudentStats:
        """
        Calculates stats for a given student ID from the sheet.
        
        Args:
            student_id (str): The Secret ID to search for.
            sheet_url (str): The Google Sheet URL.
            
        Returns:
            StudentStats: The calculated statistics.
            
        Raises:
            ValueError: If student not found or data error.
        """
        df = self.gateway.fetch_data(sheet_url)
        
        # Filter for the student
        # We look in the 'Student_ID' column (assuming it's column A or named 'Student_ID')
        if "Student_ID" not in df.columns:
            raise ValueError("Invalid Sheet Format: 'Student_ID' column missing.")
            
        # Filter rows
        student_row = df[df["Student_ID"] == student_id]
        
        if student_row.empty:
            raise ValueError(f"Student ID '{student_id}' not found.")
            
        # Extract the single row as a Series
        # iloc[0] gives us the first match
        row = student_row.iloc[0]
        
        # Calculate Logic
        # 1. Identify Date Columns:
        # We enforce Strict Validation: Must match DD/MM/YYYY regex
        import re
        # Regex for DD/MM/YYYY (simple validation)
        # \d{2} matches 01-31, \d{2} matches 01-12, \d{4} matches 2024...
        date_pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")
        
        date_columns = []
        for col in df.columns:
            if col == "Student_ID":
                continue
            
            if date_pattern.match(str(col).strip()):
                date_columns.append(col)
            else:
                # Log or just ignore non-date columns (like 'Notes')
                pass    
        
        total_lessons = 0
        present_count = 0
        
        for col in date_columns:
            val = str(row[col]).strip().upper()
            
            # We ignore empty columns or future dates if marked explicitly as such, 
            # but for MVP we assume all columns present are valid past lessons.
            # If a cell is NaN (pandas), string conversion makes it 'nan'.
            # If it is None, it makes 'None'.
            if val in ['NAN', 'NONE', '']:
                continue
                
            total_lessons += 1
            if val == 'P':
                present_count += 1
                
        percentage = 0.0
        if total_lessons > 0:
            percentage = (present_count / total_lessons) * 100
            
        return StudentStats(
            student_id=student_id,
            present_count=present_count,
            total_lessons=total_lessons,
            percentage=round(percentage, 1)
        )
