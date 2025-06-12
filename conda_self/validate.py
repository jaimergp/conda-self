import sys
from functools import cache
from importlib.metadata import entry_points

from conda.exceptions import CondaValueError


@cache
def conda_plugin_packages():
    if sys.version_info < (3, 12):
        raise RuntimeError("This function requires Python 3.12+")
    return set(
        name
        for ep in entry_points(group="conda")
        if (name := ep.dist.name.strip())  # EntryPoint.dist() only available in py312+
        and name != "conda-self"
    )


def validate_plugin_name(name: str) -> None:
    if name not in conda_plugin_packages():
        raise CondaValueError(
            f"Package '{name}' does not seem to be a valid conda plugin. Try one of:\n- "
            + "\n- ".join(sorted(conda_plugin_packages()))
        )
