from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Reset 'base' environment to essential packages only."


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.description = HELP
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    print("Resetting 'base' environment...")
    return 0
