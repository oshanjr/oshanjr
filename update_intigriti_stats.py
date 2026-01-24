import os
import requests
import re
import sys

# --- CONFIGURATION ---
# Authentication Endpoint (from your docs)
AUTH_URL = "https://login.intigriti.com/connect/token"
# Data Endpoint (Standard Researcher API)
STATS_URL = "https://api.intigriti.com/external/researcher/v1/stats"

# Load Secrets
CLIENT_ID = os.environ.get("INTIGRITI_CLIENT_ID")
CLIENT_SECRET = os.environ.get("INTIGRITI_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("INTIGRITI_REFRESH_TOKEN")

def get_access_token():
    """Exchanges the Refresh Token for a new Access Token."""
    print("🔄 Refreshing Access Token...")
    
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    
    try:
        response = requests.post(AUTH_URL, data=payload)
        response.raise_for_status() # Raise error for 400/401/403/500
        
        data = response.json()
        print("✅ Access Token refreshed successfully!")
        return data.get("access_token")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Auth Failed: {e}")
        print(f"Response: {response.text}")
        sys.exit(1)

def get_stats(access_token):
    """Fetches researcher stats using the fresh Access Token."""
    print("📊 Fetching Stats...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(STATS_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Stats Fetch Failed: {e}")
        print(f"Response: {response.text}")
        sys.exit(1)

def update_readme(rank, reputation, impact):
    """Updates the README file with new stats."""
    print("📝 Updating README...")
    
    readme_path = "README.md"
    try:
        with open(readme_path, "r") as file:
            readme = file.read()

        # HTML block for the stats
        stats_html = f"""<p align="center">
  <img src="https://img.shields.io/badge/Intigriti_Rank-{rank}-36499B?style=for-the-badge&logo=intigriti&logoColor=white" />
  <img src="https://img.shields.io/badge/Reputation-{reputation}-009A74?style=for-the-badge&logo=intigriti&logoColor=white" />
  <img src="https://img.shields.io/badge/Impact-{impact}-FF6C37?style=for-the-badge&logo=fire&logoColor=white" />
</p>
"""

        # Regex to find the block between the comments
        pattern = r".*"
        
        # Check if markers exist
        if not re.search(pattern, readme, re.DOTALL):
            print("⚠️ Markers not found in README. Please add and ")
            return

        new_readme = re.sub(pattern, stats_html, readme, flags=re.DOTALL)

        with open(readme_path, "w") as file:
            file.write(new_readme)
            
        print("✅ README updated!")

    except FileNotFoundError:
        print("❌ README.md not found!")

if __name__ == "__main__":
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("❌ Missing Secrets! Please check GitHub Settings.")
        sys.exit(1)

    # 1. Get new token
    token = get_access_token()
    
    # 2. Get data
    stats = get_stats(token)
    
    # 3. Parse data (Safe defaults if keys are missing)
    my_rank = stats.get("rank", "Unranked")
    my_rep = stats.get("reputation", 0)
    my_impact = stats.get("impact", 0)
    
    # 4. Update file
    update_readme(my_rank, my_rep, my_impact)
