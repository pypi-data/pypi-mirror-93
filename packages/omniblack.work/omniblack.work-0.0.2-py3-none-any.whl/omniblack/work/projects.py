from itertools import chain
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

print = pp.pprint


try:
    from .github_projects import projects
    gh_projs = projects()
except ImportError:
    gh_projs = tuple()

try:
    from .gitlab_projects import projects
    gl_projs = projects()
except ImportError:
    gl_projs = tuple()

projects = dict(chain(gh_projs, gl_projs))
