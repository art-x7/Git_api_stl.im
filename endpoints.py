from enum import Enum


class GitHubEndpoints(Enum):
    repo_url = "https://api.github.com/repos/%s/%s"
    pulls = "/pulls"
    issues = "/issues"
    forks = "/forks"
