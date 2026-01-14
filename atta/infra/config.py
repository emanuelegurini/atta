import json
import os
from pathlib import Path
from typing import Optional

class ConfigManager:
    """
    Manages local configuration persistence.
    Stores the student ID so the user doesn't have to re-type it every time.
    """
    
    CONFIG_DIR = Path.home() / ".atta"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self):
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        """Creates the config directory if it doesn't exist."""
        if not self.CONFIG_DIR.exists():
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
    def save_student_id(self, student_id: str):
        """Saves the student ID to config."""
        config = self._load_raw_config()
        config["student_id"] = student_id
        
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f)
            
    def get_student_id(self) -> Optional[str]:
        """Retrieves the stored student ID, or None if not set."""
        config = self._load_raw_config()
        return config.get("student_id")
        
    def _load_raw_config(self) -> dict:
        """Helper to load the JSON file safely."""
        if not self.CONFIG_FILE.exists():
            return {}
        try:
            with open(self.CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
