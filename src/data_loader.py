
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

def fetch_team_stats_for_season(team_name, season):
	# Check if data already exists (teamname_season_stats.json)
	filename = f"data/{team_name.replace('/', '_')}_{season}_stats.json"
	if os.path.exists(filename):
		with open(filename, 'r') as f:
			return json.load(f)
	
	url = f"{BASE_URL}/stats/team/season?season={season}&team={team_name}"
	response = requests.get(url, headers=HEADERS)
	if response.status_code == 200:
		try:
			data = response.json()
			data = data[0] if isinstance(data, list) and len(data) > 0 else data
		except Exception as e:
			print(f"Error decoding JSON for {team_name} in {season}: {e}")
			print(f"Response text: {response.text}")
			return None
		with open(filename, 'w') as f:
			json.dump(data, f, indent=4)
		return data
	else:
		print(f"Failed to fetch stats for {team_name} in {season}: {response.status_code}")
		print(f"Response text: {response.text}")
		return None

def fetch_team_shooting_stats_for_season(team_name, season):
	# Check if data already exists (teamname_season_shooting_stats.json)
	filename = f"data/{team_name.replace('/', '_')}_{season}_shooting_stats.json"
	if os.path.exists(filename):
		with open(filename, 'r') as f:
			return json.load(f)
	
	url = f"{BASE_URL}/stats/team/shooting/season?season={season}&team={team_name}"
	response = requests.get(url, headers=HEADERS)
	if response.status_code == 200:
		data = response.json()
		data = data[0] if isinstance(data, list) and len(data) > 0 else data
		with open(filename, 'w') as f:
			json.dump(data, f, indent=4)
		return data
	else:
		print(f"Failed to fetch shooting stats for {team_name} in {season}: {response.status_code}")
		return None

if __name__ == "__main__":
	ratings = fetch_team_ratings()
	for key, value in ratings.items():
		filename = f"data/{key.replace('/', '_')}.json"
		with open(filename, 'w') as f:
			json.dump(value, f, indent=4)
	
