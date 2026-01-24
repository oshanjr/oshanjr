import os
import requests
import re

# 1. Get the Token from GitHub Secrets
TOKEN = os.environ.get("INTIGRITI_TOKEN")
USER_ID = "oshanjr" # Your username/ID

# 2. Fetch Data from Intigriti API
# Note: Verify this endpoint in Intigriti API Docs!
API_URL = "https://api.intigriti.com/external/researcher/v1/stats" 
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

def update_readme(rank, reputation, impact):
    with open("README.md", "r") as file:
        readme = file.read()

    # Create the badges using the live data
    stats_markdown = f"""
<p align="center">
  <img src="https://img.shields.io/badge/Intigriti_Rank-{rank}-36499B?style=for-the-badge&logo=intigriti&logoColor=white" />
  <img src="https://img.shields.io/badge/Reputation-{reputation}-009A74?style=for-the-badge&logo=intigriti&logoColor=white" />
  <img src="https://img.shields.io/badge/Impact-{impact}-FF6C37?style=for-the-badge&logo=fire&logoColor=white" />
</p>
"""

    # Replace the text between the markers
    pattern = r".*"
    replacement = f"{stats_markdown}"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

    with open("README.md", "w") as file:
        file.write(new_readme)

if __name__ == "__main__":
    try:
        # Example Request (You might need to adjust based on specific API response structure)
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Extract your stats (Adjust keys based on actual JSON response)
            my_rank = data.get('rank', 'N/A')
            my_rep = data.get('reputation', '0')
            my_impact = data.get('impact', '0')
            
            update_readme(my_rank, my_rep, my_impact)
            print("README updated successfully!")
        else:
            print(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
