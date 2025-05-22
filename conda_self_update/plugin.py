"""
Plugin definition for 'conda self-update' subcommand.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conda import plugins

from .cli import configure_parser, execute

if TYPE_CHECKING:
    from collections.abc import Iterable


@plugins.hookimpl
def conda_subcommands() -> Iterable[plugins.CondaSubcommand]:
    yield plugins.CondaSubcommand(
        name="self-update",
        action=execute,
        configure_parser=configure_parser,
        summary="Performs 'conda' updates in the 'base' environment.",
    )
