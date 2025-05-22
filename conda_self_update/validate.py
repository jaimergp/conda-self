from functools import cache
from importlib.metadata import entry_points

from conda.exceptions import CondaValueError


@cache
def conda_plugin_packages():
    return set(
        name
        for ep in entry_points()
        if ep.group == "conda"
        and (name := ep.dist.name.strip())
        and name != "conda-self-update"
    )


def validate_plugin_name(name: str) -> None:
    if name not in conda_plugin_packages():
        raise CondaValueError(
            f"Package '{name}' does not seem to be a valid conda plugin. Try one of:\n- "
            + "\n- ".join(sorted(conda_plugin_packages()))
        )
