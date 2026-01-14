from dataclasses import dataclass

@dataclass
class StudentStats:
    """
    Represents the calculated statistics for a specific student.
    
    Attributes:
        student_id (str): The unique secret ID of the student.
        present_count (int): Number of lessons present.
        total_lessons (int): Total number of valid lessons processed.
        percentage (float): Attendance percentage (0.0 to 100.0).
    """
    student_id: str
    present_count: int
    total_lessons: int
    percentage: float

@dataclass
class AttendanceRecord:
    """
    Represents a raw row from the attendance sheet.
    Useful for type hinting if we need to pass single records around,
    although we primarily work with DataFrames.
    """
    student_id: str
    raw_data: dict  # Contains date: status mappings
