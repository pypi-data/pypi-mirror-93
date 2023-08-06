from pkg_resources import resource_filename
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(prog='wrk-file')
    parser.add_argument('file')

    args = parser.parse_args()

    print(resource_filename('omniblack.work', args.file))

