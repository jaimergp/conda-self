from __future__ import annotations

from typing import TYPE_CHECKING

from conda.exceptions import CondaValueError

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
    from ..install import install_specs_in_protected_env, uninstall_specs_in_protected_env
    from ..validate import validate_plugin_is_installed
    from ..query import check_installed

    print("Installing plugins:", *args.specs)

    result = install_specs_in_protected_env(
        args.specs,
        force_reinstall=args.force_reinstall,
        json=False,
    )

    # if the install has failed, make sure we are still in a good state
    if result != 0:
        print(f"Error installing requested packages into the base environment")
        return result

    non_plugin_specs = []
    for spec in args.specs:
        # ensure that the spec is installed
        installed = check_installed(spec)
        if installed is not None:
            try:
                # ensure the spec is a plugin
                validate_plugin_is_installed(spec)
            except CondaValueError:
                non_plugin_specs.append(spec)

    if len(non_plugin_specs) > 0:
        print(
              f"""
            WARNING: The following specs are not plugins: {non_plugin_specs}.
            Rolling back!
            """)
        uninstall_specs_in_protected_env(non_plugin_specs)