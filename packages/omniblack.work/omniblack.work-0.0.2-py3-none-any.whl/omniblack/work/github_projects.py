from github import Github
from config import config


def projects():
    keys = config['keys']
    if 'Github' not in keys:
        return

    github = Github(keys.Github)
    for repo in github.get_user().get_repos():
        yield repo.name, {'url': repo.ssh_url, 'desc': repo.description}
