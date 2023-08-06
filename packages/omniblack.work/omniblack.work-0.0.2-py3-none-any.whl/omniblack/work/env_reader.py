from re import compile
from box import Box

line_regex = compile('export (?P<name>.+?)=(?P<value>.+?);\n?')


def env_vars(url):
    try:
        with open(url) as file:
            exported_vars = Box()
            for line in file:
                result = line_regex.fullmatch(line)
                if result:
                    name = result.group('name')
                    value = result.group('value')
                    exported_vars[name] = value
            return exported_vars
    except FileNotFoundError:
        # TODO: Fire an error
        return Box()
