import pandas as pd
import sys

# We define the URL constant here for quick access during debugging
SHEET_URL = "https://docs.google.com/spreadsheets/d/1MrJJuqdhv5apVzXwa1AT32XnD8t_amrJNNjkYm_pOyU/export?format=csv"

def verify_connection():
    """
    Tries to connect to the Google Sheet via pandas and print the head.
    This serves as a sanity check for internet connection and file permissions.
    """
    print(f"📡 Connecting to Google Sheet: {SHEET_URL}")
    
    try:
        # We use pandas directly as it handles the CSV download and parsing 
        # in a single robust call.
        df = pd.read_csv(SHEET_URL)
        
        print("✅ Connection successful!")
        print(f"📊 Columns found: {list(df.columns)}")
        print("👀 First 5 rows preview:")
        print(df.head())
        
        # Validation: Check if 'Student_ID' exists as per specs
        if "Student_ID" not in df.columns:
            print("⚠️  WARNING: 'Student_ID' column not found! Check your sheet headers.")
        else:
            print("✅ 'Student_ID' column confirmed.")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_connection()
