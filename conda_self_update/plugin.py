"""
Insert your plugin hook definitions

We have illustrated how this is done by defining a simple "hello conda"
subcommand for you.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conda import plugins
from conda.base.context import context
from conda.common.path import paths_equal
from conda.exceptions import CondaValueError

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable


def self_update(args: Namespace) -> None:
    if paths_equal(context.target_prefix, context.root_prefix):
        raise CondaValueError("Target environment must be base.")
    print("Hello conda!")


@plugins.hookimpl
def conda_subcommands() -> Iterable[plugins.CondaSubcommand]:
    yield plugins.CondaSubcommand(
        name="self-update",
        action=self_update,
        summary="Performs 'conda' updates in the 'base' environment.",
    )
