from .config import config
from argparse import ArgumentParser
from argcomplete import autocomplete
from shutil import rmtree
from os import listdir, chdir
from git import Repo
from git.exc import InvalidGitRepositoryError
from subprocess import run
from sys import exit


def create_parser(config):
    envs = listdir(config['prefix'])
    epilog = 'Remove a work environment, and cleanup from it.'
    parser = ArgumentParser(epilog=epilog)
    parser.add_argument(
        'environment',
        choices=envs,
        metavar='environment',
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        dest='force'
    )
    autocomplete(parser)
    return parser


def is_dirty(repo):
    unpublished_commits = 0
    for branch in repo.branches:
        tracking_branch = branch.tracking_branch()
        unpublished_commits += len(list(
            repo.iter_commits(f'{tracking_branch.name}...{branch.name}')
        ))
    return unpublished_commits or repo.is_dirty(untracked_files=True)


def main():
    parser = create_parser(config)
    args = parser.parse_args()
    forced = args.force
    env = args.environment
    env_dir = f'{config.prefix}/{env}'
    try:
        repo = Repo(env_dir)
        if is_dirty(repo) and not forced:
            print(f'{env} is dirty. Refusing to remove without --force.')
    except InvalidGitRepositoryError:
        pass
    chdir(env_dir)
    try:
        run(f'{env_dir}/devtools/rmwrk.ext', check=True)
    except FileNotFoundError:
        pass
    except OSError as err:
        exec_format_error = 8
        if err.errno == exec_format_error:
            print('rmwrk.ext is not a valid executable file.')
            exit(1)
        else:
            raise

    rmtree(env_dir, ignore_errors=False)
    print(f'Removed {env}')
