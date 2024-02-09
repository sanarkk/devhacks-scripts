import os
from dotenv import load_dotenv
import requests

load_dotenv()

GITHUB_KEY = os.getenv("GITHUB_KEY")
API_BASE_URL = "https://api.github.com"


def main():
    teams = [
        [
            {
                "username": "sanarkk",
            },
        ],
    ]
    teams_counter = 0

    if not GITHUB_KEY:
        print("Organization credential key was not inserted.")
    for team in teams:
        team_data = {
            "name": f"Repository-number-{teams_counter} team.",
            "description": f"Team's number {teams_counter} description team.",
            "permission": "push",
        }
        team_request = requests.post(
            f"{API_BASE_URL}/orgs/devhacks-2024/teams",
            headers={
                "Authorization": f"Bearer {GITHUB_KEY}"
            },
            json=team_data,
        )
        team_request_parsed = team_request.json()
        if team_request.status_code == 201:
            print("Team was created")

        for member in team:
            team_member_request = requests.put(
                f"{API_BASE_URL}/teams/{team_request_parsed['id']}/memberships/{member['username']}",
                headers={
                    "Authorization": f"Bearer {GITHUB_KEY}"
                },
                json={
                    "role": "maintainer"
                }
            )
            if team_member_request.status_code == 200:
                print("Invitation has been sent.")

        repository_data = {
            "name": f"Repository-number-{teams_counter}",
            "description": f"Team's number {teams_counter} description",
            "private": False,
            "team_id": team_request_parsed["id"]
        }
        repository_request = requests.post(
            f"{API_BASE_URL}/orgs/devhacks-2024/repos",
            headers={
                "Authorization": f"Bearer {GITHUB_KEY}",
            },
            json=repository_data,
        )

        if repository_request.status_code == 201:
            print("Repository was created.")
            teams_counter += 1
        else:
            print("Repository was not created.")


if __name__ == "__main__":
    main()
