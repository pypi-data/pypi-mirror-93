#! /usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from os.path import expandvars
from argparse import ArgumentParser
from pathlib import Path

from pkg_resources import resource_stream
from ruamel.yaml import YAML
from requests import get

from omniblack.path import ProgramFiles

from .env_reader import env_vars

name = 'work'
files = ProgramFiles(name)


yaml = YAML(typ='safe', pure=True)

pool = ThreadPoolExecutor(max_workers=5)


def get_default_config():
    return resource_stream('omniblack.work', 'work/default_config.yaml')


def get_remotes(remotes_url):
    response = get(remotes_url, stream=True)
    response.raw.decode_content = True
    return yaml.load(response.raw)


def expand(path):
    return Path(expandvars(path)).expanduser()


class Config(dict):
    def __init__(self, values):
        keys = expand(values['keys'])
        del values['keys']
        self.__keys_future = pool.submit(env_vars, keys)
        self['keys'] = None

        remotes = expand(values['remotes'])
        del values['remotes']
        self.__remotes_future = pool.submit(get_remotes, remotes)
        self['remotes'] = None

        for key, value in values.items():
            self[key] = expand(value)

    def __getitem__(self, key):
        if key == 'keys':
            return self.keys
        elif key == 'remotes':
            return self.remotes
        else:
            return super().__getitem__(key)

    @property
    def remotes(self):
        remotes = self.__remotes_future.result()
        return remotes

    @property
    def keys(self):
        keys = self.__keys_future.result()
        return keys

    def replace_keys(self, keys):
        self['keys'] = keys.result()

    def replace_remotes(self, remotes):
        self['remotes'] = remotes.result()


def copy_default_config(self):
    try:
        default_config_file = get_default_config()
        config_file = files.get_config_file(name)
        config_file.config_file_sync(default_config_file, mode='wb')
        return True
    except FileExistsError:
        return False


def init_config():
    try:
        file = files.get_config_file(name)
        return Config(file.get_data_sync())
    except FileNotFoundError:
        copy_default_config()
        return init_config()
    except PermissionError:
        print(f'This program needs premission to write to {file.path}')
        raise SystemExit


config = init_config()


def main():
    parser = ArgumentParser(description='Get value out of the'
                            ' configuration of work')
    parser.add_argument('key', choices=list(config))
    args = parser.parse_args()
    value = config[args.key]
    print(value)


if __name__ == '__main__':
    main()
