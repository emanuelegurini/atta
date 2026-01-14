import os
import questionary
import sys
from atta.core.service import AttendanceService
from atta.infra.config import ConfigManager
from atta.ui import console

# CONSTANT: The Public Sheet URL (Loaded from .env)
SHEET_URL = os.getenv("ATTA_SHEET_URL")

class MainMenu:
    """
    The main interaction loop of the application.
    """
    
    def __init__(self):
        self.config = ConfigManager()
        self.service = AttendanceService()
        
    def start(self):
        console.print_banner()
        
        if not SHEET_URL:
            console.print_error("Configuration Error: ATTA_SHEET_URL not found in .env file.")
            sys.exit(1)
            
        # Action Dispatch Map
        actions = {
            "📊 View My Stats": self._handle_view_stats,
            "⚙️  Settings (Change ID)": self._handle_settings,
            "❌ Exit": self._handle_exit
        }
        
        # Main Application Loop
        while True:
            choice = questionary.select(
                "What would you like to do?",
                choices=list(actions.keys())
            ).ask()
            
            if choice is None: # Handle Ctrl+C
                self._handle_exit()
                
            # Execute the selected action
            handler = actions.get(choice)
            if handler:
                handler()

    def _handle_exit(self):
        console.print_success("Bye! 👋")
        sys.exit(0)

    def _handle_view_stats(self):
        # 1. Get ID (from config or ask)
        student_id = self.config.get_student_id()
        
        if not student_id:
            console.print_error("No Student ID found.")
            if questionary.confirm("Do you want to set your ID now?").ask():
                self._handle_settings()
                student_id = self.config.get_student_id() # Reload
            else:
                return

        if not student_id:
            return

        # 2. Fetch & Show
        try:
            with console.show_loading("Fetching data from Google Sheets..."):
                stats = self.service.get_stats_for_student(student_id, SHEET_URL)
            
            console.print_stats_table(stats)
            
            # Pause so user can see result before menu clears/redraws
            questionary.press_any_key_to_continue().ask()
            
        except ValueError as e:
            console.print_error(str(e))
        except Exception as e:
            console.print_error(f"Unexpected error: {e}")

    def _handle_settings(self):
        current_id = self.config.get_student_id() or "None"
        print(f"Current ID: {current_id}")
        
        new_id = questionary.text("Enter your Secret Student ID:").ask()
        
        if new_id:
            self.config.save_student_id(new_id.strip())
            console.print_success(f"ID saved as: {new_id}")
        else:
            console.print_error("Operation cancelled.")
