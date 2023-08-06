#!/usr/local/bin/python3
import sys

from maven_version import error, MavenVersion


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        error('Invalid arguments\n\t')

    v1 = MavenVersion(args[0])
    v2 = MavenVersion(args[1])
    print(1 if v1 > v2 else -1 if v1 < v2 else 0, end='')


if __name__ == '__main__':
    main()
