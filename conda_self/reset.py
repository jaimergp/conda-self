import sys
from conda.core.prefix_data import PrefixData
from conda.core.link import PrefixSetup, UnlinkLinkTransaction
from conda.base.context import context

from .query import permanent_dependencies


def reset(prefix: str = sys.prefix, uninstallable_packages: list[str] = []):
    installed = sorted(PrefixData(prefix).iter_records(), key=lambda x: x.name)
    packages_to_remove = [pkg for pkg in installed if pkg.name not in uninstallable_packages]

    stp = PrefixSetup(
        target_prefix=prefix,
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
