from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Remove conda plugins from the 'base' environment."


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.add_argument("specs", nargs="+", help="Plugins to install")
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    print("Removing plugins:", *args.specs)
    return 0
