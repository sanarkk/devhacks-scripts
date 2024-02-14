import os
import requests

from dotenv import load_dotenv

load_dotenv()

GITHUB_KEY = os.getenv("GITHUB_KEY")
API_BASE_URL = "https://api.github.com"
PRESENTATION_BRANCH_NAME = "presentation_branch"


def main() -> any:
    organization_repositories = []
    presentation_repositories = []

    org_repos = requests.get(
        url=f"{API_BASE_URL}/orgs/devhacks-2024/repos",
        headers={
            "Authorization": f"Bearer {GITHUB_KEY}"
        },
    )
    org_repos_converted = org_repos.json()
    for repository in org_repos_converted:
        organization_repositories.append(
            {
                "repo_name": repository["name"],
                "repo_url": repository["html_url"]
            }
        )

    for repository in organization_repositories:
        repository_to_check = requests.get(
            url=f"{API_BASE_URL}/repos/devhacks-2024/{repository['repo_name']}/branches",
            headers={
                "Authorization": f"Bearer {GITHUB_KEY}"
            },
        )
        repository_to_check_converted = repository_to_check.json()
        if repository_to_check_converted:
            if repository_to_check_converted[0]["name"] == PRESENTATION_BRANCH_NAME:
                presentation_repositories.append(repository["repo_url"])


if __name__ == "__main__":
    main()
