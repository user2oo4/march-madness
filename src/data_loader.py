
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('college_basketball_data_api_key')
BASE_URL = os.getenv('college_basketball_data', 'https://api.collegebasketballdata.com')

HEADERS = {
	'Authorization': f'Bearer {API_KEY}'
}

def fetch_team_ratings():
	"""
	Fetch team ratings (srs, adjusted, elo)
	"""
	rating_types = ['ratings/srs', 'ratings/adjusted', 'ratings/elo']
	results = {}
	for rating in rating_types:
		url = f"{BASE_URL}/{rating}"
		response = requests.get(url, headers=HEADERS)
		if response.status_code == 200:
			results[rating] = response.json()
		else:
			print(f"Failed to fetch {rating}: {response.status_code}")
			results[rating] = None
	return results

if __name__ == "__main__":
	ratings = fetch_team_ratings()
	for key, value in ratings.items():
		filename = f"data/{key.replace('/', '_')}.json"
		with open(filename, 'w') as f:
			json.dump(value, f, indent=4)
	
