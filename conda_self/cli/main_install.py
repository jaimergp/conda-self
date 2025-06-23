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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report available updates, do not install.",
    )
    parser.add_argument("specs", nargs="+", help="Plugins to install")
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    import sys

    from conda.api import Solver, PackageCacheData
    from conda.base.context import context
    from conda.cli.common import stdout_json_success
    from conda.common.path import is_package_file
    from conda.exceptions import CondaValueError, DryRunExit
    from conda.models.match_spec import MatchSpec
    from conda.misc import _match_specs_from_explicit
    from conda.reporters import confirm_yn

    from ..exceptions import SpecsAreNotPlugins
    from ..package_info import PackageInfo

    print("Installing plugins:", *args.specs)

    specs_to_add = []

    num_cp = sum(is_package_file(s) for s in args.specs)
    if num_cp:
        if num_cp == len(args.specs):
            specs_to_add = list(_match_specs_from_explicit(args.specs))
        else:
            raise CondaValueError(
                "cannot mix specifications with conda package filenames"
            )
    else:
        specs_to_add = [MatchSpec(spec) for spec in args.specs]

    solver = Solver(
        sys.prefix, context.channels, specs_to_add=specs_to_add
    )
    transaction =  solver.solve_for_transaction()
    transaction.download_and_extract()

    specs_to_add_names = [spec.name for spec in specs_to_add]
    link_precs = [precs for precs in transaction.prefix_setups[sys.prefix].link_precs if precs.name in specs_to_add_names]    
    package_cache_records = [PackageCacheData.query_all(prec)[0] for prec in link_precs]
    invalid_specs = []
    for pcr in package_cache_records:
        info =  PackageInfo.from_conda_extracted_package_path(pcr.extracted_package_dir)
        if "conda" not in info.entry_points().keys():
            invalid_specs.append(pcr.name)
    
    if invalid_specs:
        raise SpecsAreNotPlugins(invalid_specs)

    if not context.json:
        transaction.print_transaction_summary()
        confirm_yn()
    elif context.dry_run:
        actions = transaction._make_legacy_action_groups()[0]
        stdout_json_success(prefix=sys.prefix, actions=actions, dry_run=True)
        raise DryRunExit()

    transaction.execute()    

    if context.json:
        actions = transaction._make_legacy_action_groups()[0]
        stdout_json_success(prefix=sys.prefix, actions=actions)

    return 0
