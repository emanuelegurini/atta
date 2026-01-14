import pandas as pd
import logging
from typing import Optional

# Configure module-level logger
logger = logging.getLogger(__name__)

class GSheetGateway:
    """
    Gateway responsible for fetching data from Google Sheets.
    It abstracts the underlying HTTP/CSV details and returns a usable pandas DataFrame.
    """

    def fetch_data(self, sheet_url: str) -> pd.DataFrame:
        """
        Fetches the content of a Google Sheet via its public export URL.
        
        Args:
            sheet_url (str): The public sharing URL of the Google Sheet.
            
        Returns:
            pd.DataFrame: The pandas DataFrame containing the sheet data.
            
        Raises:
            ValueError: If the URL is invalid or the fetch fails.
        """
        export_url = self._convert_to_export_url(sheet_url)
        logger.info(f"📡 Fetching data from: {export_url}")

        try:
            # Pandas read_csv handles the HTTP request and CSV parsing
            df = pd.read_csv(export_url)
            
            # Basic validation
            if df.empty:
                logger.warning("⚠️  Fetched DataFrame is empty.")
            
            logger.info(f"✅ Successfully loaded {len(df)} rows.")
            return df

        except Exception as e:
            logger.error(f"❌ Failed to fetch data: {e}")
            raise ValueError(f"Could not fetch data from Google Sheet: {e}")

    def _convert_to_export_url(self, url: str) -> str:
        """
        Helper to ensure we have the correct CSV export URL.
        """
        if "/export?format=csv" in url:
            return url
            
        # If it's a standard edit URL, strip everything after /edit and replace
        if "/edit" in url:
            base_url = url.split("/edit")[0]
            return f"{base_url}/export?format=csv"
            
        # Fallback: if we just received the base ID url without edit or export
        # This is a best-effort guess
        return f"{url}/export?format=csv"
