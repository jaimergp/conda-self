from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Protect 'base' environment from any further modifications"


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    print("Protecting 'base' environment...")
    return 0
