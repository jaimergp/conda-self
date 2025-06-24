from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Reset 'base' environment to essential packages only."


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    import sys

    from conda.core.prefix_data import PrefixData
    from conda.core.link import PrefixSetup, UnlinkLinkTransaction
    from conda.base.context import context

    from ..query import permanent_dependencies

    print("Resetting 'base' environment...")

    installed = sorted(PrefixData(sys.prefix).iter_records(), key=lambda x: x.name)
    uninstallable_packages = permanent_dependencies()
    packages_to_remove = [pkg for pkg in installed if pkg.name not in uninstallable_packages]

    stp = PrefixSetup(
        target_prefix=sys.prefix,
        unlink_precs=packages_to_remove,
        link_precs=(),
        remove_specs=(),
        update_specs=(),
        neutered_specs=(),
    )

    txn = UnlinkLinkTransaction(stp)
    if not context.json and not context.quiet:
        txn.print_transaction_summary()
    txn.execute()
    return 0
