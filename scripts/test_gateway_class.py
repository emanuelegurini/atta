import sys
import os

# Add project root to path so we can import atta
sys.path.append(os.getcwd())

from atta.core.gateway import GSheetGateway

SHEET_URL = "https://docs.google.com/spreadsheets/d/1MrJJuqdhv5apVzXwa1AT32XnD8t_amrJNNjkYm_pOyU/edit?usp=sharing"

def test_gateway():
    print("🧪 Testing GSheetGateway...")
    gateway = GSheetGateway()
    
    try:
        df = gateway.fetch_data(SHEET_URL)
        print("✅ Gateway returned a DataFrame!")
        print(f"📊 Shape: {df.shape}")
        print("👀 Head:")
        print(df.head())
        
        # Verify columns again
        if "Student_ID" in df.columns:
            print("✅ 'Student_ID' column found.")
        else:
            print("❌ 'Student_ID' missing.")
            
    except Exception as e:
        print(f"❌ Gateway failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_gateway()
