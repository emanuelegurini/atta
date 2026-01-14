import pytest
import pandas as pd
from unittest.mock import MagicMock
from atta.core.service import AttendanceService
from atta.core.gateway import GSheetGateway
from atta.core.models import StudentStats

# Fixture for a mock gateway
@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=GSheetGateway)
    return gateway

@pytest.fixture
def service(mock_gateway):
    return AttendanceService(gateway=mock_gateway)

def test_attendance_calculation_all_present(service, mock_gateway):
    # Setup Data: Student present in 2 lessons
    data = {
        "Student_ID": ["S-100", "S-101"],
        "01/01/2024": ["P", "A"],
        "02/01/2024": ["P", "P"]
    }
    df = pd.DataFrame(data)
    mock_gateway.fetch_data.return_value = df
    
    stats = service.get_stats_for_student("S-100", "http://fake")
    
    assert stats.student_id == "S-100"
    assert stats.total_lessons == 2
    assert stats.present_count == 2
    assert stats.percentage == 100.0

def test_attendance_calculation_mixed(service, mock_gateway):
    # Setup Data: 1 Present, 1 Absent (A), 1 Absent (Generic/Empty is handled?)
    # Our logic says: 'nan' is skip, 'A' counts as lesson but not present.
    data = {
        "Student_ID": ["S-100"],
        "01/01/2024": ["P"],
        "02/01/2024": ["A"],
        "03/01/2024": ["Foo"] # Not P, so absent
    }
    df = pd.DataFrame(data)
    mock_gateway.fetch_data.return_value = df
    
    stats = service.get_stats_for_student("S-100", "http://fake")
    
    assert stats.total_lessons == 3
    assert stats.present_count == 1
    assert stats.percentage == 33.3

def test_student_not_found(service, mock_gateway):
    df = pd.DataFrame({"Student_ID": ["S-999"]})
    mock_gateway.fetch_data.return_value = df
    
    with pytest.raises(ValueError, match="not found"):
        service.get_stats_for_student("S-100", "http://fake")

def test_ignore_empty_cells(service, mock_gateway):
    # Test that empty cells (NaN) are ignored from total count
    data = {
        "Student_ID": ["S-100"],
        "01/01/2024": ["P"],
        "02/01/2024": [None] # pandas NaN
    }
    df = pd.DataFrame(data)
    mock_gateway.fetch_data.return_value = df
    
    stats = service.get_stats_for_student("S-100", "http://fake")
    
    # Total should be 1, because FutureLesson is NaN/Empty
    assert stats.total_lessons == 1
    assert stats.percentage == 100.0

def test_ignore_non_date_columns(service, mock_gateway):
    # Test that columns like 'Notes' or 'Total' are ignored
    data = {
        "Student_ID": ["S-100"],
        "01/01/2024": ["P"],
        "Notes": ["Great student"],
        "Total": ["100"]
    }
    df = pd.DataFrame(data)
    mock_gateway.fetch_data.return_value = df
    
    stats = service.get_stats_for_student("S-100", "http://fake")
    
    # Only 01/01/2024 should count
    assert stats.total_lessons == 1
    assert stats.present_count == 1
    assert stats.percentage == 100.0
