import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/grundy/PycharmProjects/diplo/.env')
api_key = os.getenv('FOOTBALL_KEY')
base_url = "https://api.football-data.org/v4/"


def get_current_scores(team_id: int) -> dict:
    headers = {
        'X-Auth-Token': api_key
    }

    url = f"{base_url}matches/330299"

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        return data["matches"]
    else:
        return {"error": f"Error fetching scores: {data['message']}"}



if __name__ == '__main__':
    print(get_current_scores(1))