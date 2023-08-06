#! /usr/bin/env python3

from argparse import ArgumentParser, SUPPRESS, RawDescriptionHelpFormatter
from .config import config
from git import Repo
from work.projects import projects
from pathlib import Path
from subprocess import run
from os import environ, chdir, getcwd
from argcomplete import autocomplete


def create_parse(projects):
    available_projects = '\n\n'.join(f'{name}: {project["desc"]}'
                                     for name, project in projects.items())
    epilog = f'Available projects are:\n {available_projects}\n'
    parser = ArgumentParser(prog="mkwrk",  epilog=epilog,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('project', choices=projects, metavar='project')
    parser.add_argument('new_environment', default=SUPPRESS, nargs='?')
    autocomplete(parser)

    return parser.parse_args()


def main():
    args = create_parse(projects)
    if 'new_environment' in args:
        path = Path(config['prefix'], args.new_environment)
    else:
        path = Path(config['prefix'], args.project)

        remote_path = projects[args.project]['url']
        Repo.clone_from(remote_path, path)

        mkwrk_ext = Path.joinpath(path, 'devtools', 'mkwrk.ext')
        if mkwrk_ext.exists():
            environ['SRC'] = str(path)
            environ['WRK_ENV'] = args.new_environment
            environ[' OLD_LOC'] = getcwd()

            chdir(path)
            run([str(mkwrk_ext)])
