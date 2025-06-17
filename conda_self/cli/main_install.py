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
    import sys

    from conda.api import Solver, PackageCacheData
    from conda.base.context import context
    from conda.cli.common import arg2spec
    from conda.exceptions import CondaValueError


    from ..validate import validate_plugin_is_installed

    print("Installing plugins:", *args.specs)

    specs_to_add = [arg2spec(spec) for spec in args.specs]
    solver = Solver(
        sys.prefix, context.channels, specs_to_add=specs_to_add
    )
    transaction =  solver.solve_for_transaction()
    transaction.download_and_extract()

    link_precs = [precs for precs in transaction.prefix_setups[sys.prefix].link_precs if precs.name in args.specs]    
    package_cache_records = [PackageCacheData.query_all(prec)[0] for prec in link_precs]
    for pcr in package_cache_records:
        # hmmm, maybe a lil wild
        sys.path.append(pcr.extracted_package_dir)
    
    invalid_specs = []
    for spec in args.specs:
        try:
            validate_plugin_is_installed(spec)
        except CondaValueError:
            invalid_specs.append(spec)
    
    if invalid_specs:
        print(f"The following requested specs are not plugins: {invalid_specs}")
        print("Aborting install!")
        return 1

    # TODO: execute transaction      
    return 0
