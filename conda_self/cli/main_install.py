from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Add conda plugins to the 'base' environment."


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.add_argument(
        "--force-reinstall",
        action="store_true",
        help="Reinstall plugin even if it's already installed.",
    )
    parser.add_argument("specs", nargs="+", help="Plugins to install")
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    print("Installing plugins:", *args.specs)
    return 0
