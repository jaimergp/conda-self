""" """

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.core.prefix_data import PrefixData
from conda.core.subdir_data import SubdirData
from conda.exceptions import (
    PackageNotInstalledError,
    PackagesNotFoundError,
)
from conda.models.channel import Channel
from conda.models.version import VersionOrder

if TYPE_CHECKING:
    from collections.abc import Iterable

    from conda.common.path import PathType
    from conda.models.records import PackageRecord, PrefixRecord


def check_updates(
    package_name: str,
    prefix: PathType = sys.prefix,
) -> tuple[bool, PrefixRecord, PackageRecord | None]:
    installed = PrefixData(prefix).get(package_name)
    if not installed:
        raise PackageNotInstalledError(prefix, package_name)

    subdir = installed.subdir
    subdirs = (subdir, (context.subdir if subdir == "noarch" else "noarch"))
    latest_available = latest(installed.name, installed.channel.base_url, subdirs)
    update_available = latest_available.version > VersionOrder(installed.version)

    return update_available, installed, latest_available


def latest(
    package_name: str, channel_url: str, subdirs: Iterable[str]
) -> PackageRecord:
    best = None
    max_version = VersionOrder("0.0.0dev0")
    channels = []
    for subdir in subdirs:
        channel = Channel(f"{channel_url}/{subdir}")
        channels.append(channel)
        for record in SubdirData(channel).query(package_name):
            if (record_version := VersionOrder(record.version)) > max_version:
                best = record
                max_version = record_version
    if best is None:
        raise PackagesNotFoundError(package_name, channels)
    return best
