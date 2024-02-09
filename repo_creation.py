import os
from dotenv import load_dotenv
import requests

load_dotenv()

GITHUB_KEY = os.getenv("GITHUB_KEY")
API_BASE_URL = "https://api.github.com"


def main() -> any:
    teams = [[{"username": "sanarkk", },],]
    teams_counter = 0

    if not GITHUB_KEY:
        print("Organization credential key was not inserted.")

    for team in teams:
        created_team = create_team(teams_counter)
        team_request_converted = convert(created_team["request"])

        for member in team:
            print(add_team_member(team_id=team_request_converted["id"], username=member["username"])["message"])

        print(create_repository(teams_counter=teams_counter, team_id=team_request_converted["id"])["message"])


def send_post_request(url: str, headers: dict, data: dict) -> any:
    return requests.post(url=url, headers=headers, json=data, )


def send_put_request(url: str, headers: dict, data: dict) -> any:
    return requests.put(url=url, headers=headers, json=data)


def convert(data: any) -> dict:
    return data.json()


def create_team(teams_counter: int) -> dict:
    team_data = {
        "name": f"Repository-number-{teams_counter} team.",
        "description": f"Team's number {teams_counter} description team.",
        "permission": "push",
    }
    team_request = send_post_request(
        url=f"{API_BASE_URL}/orgs/devhacks-2024/teams",
        headers={
            "Authorization": f"Bearer {GITHUB_KEY}"
        },
        data=team_data
    )
    if team_request.status_code == 201:
        return {
            "request": team_request
        }
    else:
        return {
            "message": "Some error occurred. Team has not been created."
        }


def add_team_member(team_id: int, username: str) -> dict:
    team_member_request = send_put_request(
        url=f"{API_BASE_URL}/teams/{team_id}/memberships/{username}",
        headers={
            "Authorization": f"Bearer {GITHUB_KEY}"
        },
        data={
            "role": "maintainer"
        }
    )
    if team_member_request.status_code == 200:
        return {
            "message": "Invitation has been sent."
        }
    else:
        return {
            "message": "Some error occurred. Invitation has not been sent."
        }


def create_repository(teams_counter: id, team_id: int) -> dict:
    repository_data = {
        "name": f"Repository-number-{teams_counter}",
        "description": f"Team's number {teams_counter} description",
        "private": False,
        "team_id": team_id
    }
    repository_request = send_post_request(
        url=f"{API_BASE_URL}/orgs/devhacks-2024/repos",
        headers={
            "Authorization": f"Bearer {GITHUB_KEY}",
        },
        data=repository_data,
    )

    if repository_request.status_code == 201:
        teams_counter += 1
        return {
            "message": "Repository has been created."
        }
    else:
        return {
            "message": "Some error occurred. Repository has not been created."
        }


if __name__ == "__main__":
    main()
