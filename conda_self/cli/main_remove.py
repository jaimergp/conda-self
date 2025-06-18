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
    from ..query import permanent_dependencies
    from ..install import uninstall_specs_in_protected_env

    uninstallable_packages = permanent_dependencies()
    for spec in args.specs:
        if spec in uninstallable_packages:
            print(f"Package '{spec}' can not be removed. Aborting!")
            return 0

    print("Removing plugins:", *args.specs)

    uninstall_specs_in_protected_env(args.specs, yes=False)
    return 0
