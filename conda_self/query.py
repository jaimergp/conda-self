""" """

from __future__ import annotations

import sys
from functools import cache
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

from .constants import PERMANENT_PACKAGES

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
    update_available = VersionOrder(latest_available.version) > VersionOrder(
        installed.version
    )

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


@cache
def permanent_dependencies() -> list[str]:
    """Get the full list of dependencies for all the permanent packages."""
    packages = []
    for pkg in PERMANENT_PACKAGES:
        packages.extend(package_dependencies(pkg))
    return set(packages)


@cache
def package_dependencies(
    package_name: str,
    prefix: PathType = sys.prefix,
) -> list[str]:
    """Get the full list of dependencies for a given package name.

    :param package_name: The name of the package to get dependencies for.
    :param prefix: The path to prefix.
    :return: A list of all the dependencies name.
    """
    try:
        package = PrefixData(prefix).get(package_name)
    except:
        return []

    if not package:
        raise PackageNotInstalledError(prefix, package_name)

    packages = []
    for dep in package.depends:
        dep_name = dep.split(" ")[0]
        packages.append(dep_name)
        packages.extend(package_dependencies(dep_name))

    return set(packages)
