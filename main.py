import sys
import os
from dotenv import load_dotenv

# Ensure we can import atta package
sys.path.append(os.getcwd())

# Load environment variables from .env file
load_dotenv()

try:
    from atta.ui.menu import MainMenu
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import application modules.\n{e}")
    sys.exit(1)

def main():
    try:
        app = MainMenu()
        app.start()
    except KeyboardInterrupt:
        print("\nSee you later!")
        sys.exit(0)

if __name__ == "__main__":
    main()
