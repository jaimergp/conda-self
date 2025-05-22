from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def configure_parser(parser: argparse.ArgumentParser) -> None:
    from . import APP_NAME, APP_VERSION

    # conda lockfiles --version
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
        help=f"Show the {APP_NAME} version number and exit.",
    )

    parser.add_argument(
        "--force-reinstall",
        action="store_true",
        help="Install latest conda available even "
        "if currently installed is more recent.",
    )
    parser.add_argument(
        "--plugin",
        help="Name of a conda plugin to update",
    )


def execute(args: argparse.Namespace) -> int:
    import sys
    from subprocess import run

    from conda.base.context import context
    from conda.reporters import get_spinner

    from .query import check_updates, validate_plugin_name

    if args.plugin:
        validate_plugin_name(args.plugin)
        package_name = args.plugin
    else:
        package_name = "conda"
    with get_spinner(f"Checking updates for {package_name}"):
        update_available, installed, latest = check_updates(package_name, sys.prefix)

    if not update_available:
        if not args.force_reinstall:
            print(f"{package_name} is already using the latest version available!")
            return 0

    if not context.quiet:
        print(f"Installed {package_name}: {installed.version}")
        print(f"Latest {package_name}: {latest.version}")

    process = run(
        [
            sys.executable,
            "-m",
            "conda",
            "install",
            f"--prefix={sys.prefix}",
            *(
                ("--override-frozen-envs",)
                if hasattr(context, "protect_frozen_envs")
                else ()
            ),
            *(("--force-reinstall",) if args.force_reinstall else ()),
            "--update-specs",
            "--override-channels",
            f"--channel={installed.channel}",
            f"{package_name}={latest.version}",
        ]
    )
    return process.returncode
