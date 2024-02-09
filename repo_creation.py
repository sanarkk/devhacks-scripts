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
                "github_email": "oleksandr.dimbrovskyi@gmail.com",
                "username": "sanarkk",
            },
        ],
    ]
    teams_counter = 0

    if not GITHUB_KEY:
        print("Organization credential key was not inserted.")

    for team in teams:
        team_members = []
        for member in team:
            member_github = requests.get(
                f"{API_BASE_URL}/users/{member['username']}",
            )
            member_github_parsed = member_github.json()
            team_members.append(f"{member_github_parsed["id"]}")

        team_data = {
            "name": f"Repository-number-{teams_counter} team.",
            "description": f"Team's number {teams_counter} description team.",
            "permission": "push",
            "maintainers": team_members,  # something wrong here, problem with adding people to the team
            # 'message': 'Invalid maintainers were specified.'
        }
        team_request = requests.post(
            f"{API_BASE_URL}/orgs/devhacks-2024/teams",
            headers={
                "Authorization": f"Bearer {GITHUB_KEY}"
            },
            json=team_data,
        )
        team_request_parsed = team_request.json()
        # print(team_request_parsed) this line describes error github api returns
        if team_request.status_code == 201:
            print("Team was created")

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
            team_members.clear()  # after the loop came through one team, it clears team_members list,
            # so other team will fill it again
        else:
            print("Repository was not created.")


if __name__ == "__main__":
    main()
