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


def execute(args: argparse.Namespace) -> int:
    import sys
    from subprocess import run

    from conda.base.context import context
    from conda.core.prefix_data import PrefixData
    from conda.core.subdir_data import SubdirData
    from conda.models.channel import Channel
    from conda.models.version import VersionOrder

    pd = PrefixData(sys.prefix)
    installed = pd.get("conda")
    assert installed
    channel = Channel(f"{installed.channel.base_url}/{installed.subdir}")
    sd = SubdirData(channel)
    latest = max(sd.query("conda"), key=lambda record: VersionOrder(record.version))
    if not context.quiet:
        print("Installed conda:", installed.version)
        print("Latest conda:", latest.version)
    if latest.version <= VersionOrder(installed.version):
        print("You are using latest conda already!")
        if args.force_reinstall:
            print("Forcing reinstall anyway")
        else:
            return 0

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
            f"conda={latest.version}",
        ]
    )
    return process.returncode
