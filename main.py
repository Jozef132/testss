import requests
import time

# API Endpoint
BASE_URL = "https://api.goblinmine.game/graphql"

# Headers
HEADERS = {
    "accept": "*/*",
    "accept-language": "ar",
    "app-b": "c8fc7cbd-0892-4d98-8022-082c069cd89c",
    "authorization": "Bearer 89187230|t2v0yHvlotPnj3PhAxlW8dYYPnpJMh2uxvdhF69ke484cbf6",  # Updated token
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}

# Function to send a GraphQL request
def send_request(payload):
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Fetch all mines
def fetch_mines(world_id):
    payload = {
        "operationName": "minesAndCheckTasksCompleted",
        "variables": {
            "worldId": world_id
        },
        "query": """
        query minesAndCheckTasksCompleted($worldId: Int!) {
            mines(worldId: $worldId) {
                id
                userMine {
                    id
                }
                __typename
            }
        }
        """
    }
    return send_request(payload)

# Claim rewards for a specific mine
def claim_rewards(mine_id, world_id):
    payload = {
        "operationName": "pickUp",
        "variables": {
            "input": {
                "mineId": mine_id,
                "worldId": world_id
            }
        },
        "query": """
        mutation pickUp($input: PickUpMineInput!) {
            pickUp(input: $input) {
                total
                __typename
            }
        }
        """
    }
    return send_request(payload)

# Main Script
if __name__ == "__main__":
    world_id = 1  # Fixed world ID

    while True:  # Infinite loop
        print("Fetching mines...")
        mines_response = fetch_mines(world_id)
        if not mines_response or "data" not in mines_response:
            print("Failed to fetch mines.")
        else:
            mines = mines_response["data"]["mines"]
            print(f"Found {len(mines)} mines.")

            for mine in mines:
                user_mine = mine.get("userMine")
                if user_mine and "id" in user_mine:
                    mine_id = user_mine["id"]
                    print(f"Claiming rewards for mine ID {mine_id}...")
                    claim_response = claim_rewards(mine_id, world_id)
                    if claim_response and "data" in claim_response:
                        total = claim_response["data"]["pickUp"]["total"]
                        print(f"Rewards claimed: {total} for mine ID {mine_id}.")
                    else:
                        print(f"Failed to claim rewards for mine ID {mine_id}.")
                else:
                    print(f"Skipping mine ID {mine['id']} (No active userMine).")

        print("Waiting for 10 seconds...")
        time.sleep(10)  # Wait for 10 seconds before the next iteration
