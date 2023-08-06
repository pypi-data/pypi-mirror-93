from gitlab import Gitlab
from config import config


def projects():
    keys = config['keys']

    if 'Gitlab' not in keys:
        return

    gitlab = Gitlab('https://gitlab.com', private_token=keys.Gitlab)
    for project in gitlab.projects.list(membership=True):
        yield (project.name, {
            'url': project.ssh_url_to_repo,
            'desc': project.attributes['description']
        })
