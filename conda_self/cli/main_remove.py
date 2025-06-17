from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Remove conda plugins from the 'base' environment."


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.add_argument("specs", nargs="+", help="Plugins to remove/uninstall")
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    from ..constants import PERMANENT_PACKAGES
    from ..install import uninstall_specs_in_protected_env

    for spec in args.specs:
        if spec in PERMANENT_PACKAGES:
            print(f"Package '{spec}' can not be removed. Aborting!")
            return 0

    print("Removing plugins:", *args.specs)

    uninstall_specs_in_protected_env(args.specs, yes=False)
    return 0
