"""
Stow, but in Python, and in a single file.
"""

import argparse
import fnmatch
import os
from os import path
import re
import shutil
import sys
from typing import Callable


__version__ = "1.0.0"


def add(args: argparse.Namespace):
    target = path.realpath(args.target)
    file_path = path.realpath(args.add)
    package = path.realpath(args.packages[0])
    if path.commonprefix([target, file_path]) != target:
        print(f"error: '{args.add}' not under '{args.target}'", file=sys.stderr)
        sys.exit(1)
    rest = file_path[len(target) + 1:]
    dest_path = path.join(package, rest)
    dest = path.dirname(dest_path)
    if args.verbose and not path.exists(dest):
        print("DIR", dest)
    os.makedirs(dest, mode=0o755, exist_ok=True)
    if args.verbose:
        print("SWAP", dest_path, file_path)
    if not args.dry_run:
        shutil.move(file_path, dest)
        # XXX Should really check if the symlink fails here.
        os.symlink(dest_path, file_path)


def install(args: argparse.Namespace, is_excluded: Callable[[str], bool]):
    for package in args.packages:
        if not path.isdir(package):
            print(f"no such package: {package}; skipping", file=sys.stderr)
            continue
        for root, _, files in os.walk(package, followlinks=True):
            files = [filename for filename in files if not is_excluded(filename)]
            if len(files) == 0:
                continue
            rest = root[len(package) + 1:]
            dest = path.join(args.target, rest)
            if rest != "":
                if args.verbose:
                    print("DIR", dest)
                if not args.dry_run and not os.path.exists(dest):
                    os.makedirs(dest, mode=0o755)
            for filename in files:
                dest_path = path.join(dest, filename)
                if path.exists(dest_path):
                    if args.verbose:
                        print("SKIP", dest_path)
                    continue
                src_path = path.realpath(path.join(root, filename))
                if args.verbose:
                    print("LINK", src_path, dest_path)
                if not args.dry_run:
                    if path.islink(dest_path):
                        if args.verbose:
                            print("DANGLE", dest_path)
                        os.unlink(dest_path)
                    os.symlink(src_path, dest_path)


def uninstall(args: argparse.Namespace, is_excluded: Callable[[str], bool]):
    dirs = []
    for package in args.packages:
        if not path.isdir(package):
            print(f"no such package: {package}; skipping", file=sys.stderr)
            continue
        for root, _, files in os.walk(package, followlinks=True):
            files = [filename for filename in files if not is_excluded(filename)]
            if len(files) == 0:
                continue
            rest = root[len(package) + 1:]
            dest = path.join(args.target, rest)
            if rest != "":
                dirs.append(dest)
            for filename in files:
                dest_path = path.join(dest, filename)
                if path.islink(dest_path):
                    src_path = path.realpath(path.join(root, filename))
                    if path.realpath(dest_path) == src_path:
                        if args.verbose:
                            print("UNLINK", dest_path)
                        if not args.dry_run:
                            os.unlink(dest_path)
                    elif args.verbose:
                        print("SKIP", dest_path)
                elif args.verbose:
                    print("SKIP", dest_path)

    # Delete the directories if empty.
    for dir_path in sorted(dirs, key=len, reverse=True):
        try:
            if args.verbose:
                print("RMDIR", dir_path)
            if not args.dry_run:
                os.rmdir(dir_path)
        except OSError:
            pass


def make_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A symlink farm manager.")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--target",
        "-t",
        default=os.curdir,
        help="Target directory in which to place symlinks",
    )
    parser.add_argument(
        "--exclude",
        "-x",
        action="append",
        default=[],
        metavar="GLOB",
        help="Glob pattern of files to exclude",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry run",
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--uninstall",
        "-D",
        action="store_false",
        dest="install",
        help="Uninstall symlinks",
    )
    group.add_argument(
        "--add",
        "-a",
        metavar="FILE",
        help="Stow files in a particular package",
    )

    parser.add_argument(
        "packages",
        metavar="PACKAGE",
        nargs="+",
        help="Packages to install",
    )
    return parser


def main():
    parser = make_argparser()
    args = parser.parse_args()
    exclude = [re.compile(fnmatch.translate(pattern)) for pattern in args.exclude]

    def is_excluded(filename):
        return any(pattern.match(filename) for pattern in exclude)

    if args.add:
        if len(args.packages) > 1:
            parser.error("--add only works with a single package")
        args.add = path.normpath(path.join(args.target, args.add))
        if not path.isfile(args.add):
            parser.error(f"no such file: {args.add}")
        add(args)
    elif args.install:
        install(args, is_excluded)
    else:
        uninstall(args, is_excluded)


if __name__ == "__main__":
    main()
