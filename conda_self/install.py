import sys
from subprocess import run

from conda.base.context import context


def install_package_in_protected_env(
    package_name: str,
    package_version: str,
    channel: str,
    force_reinstall: bool = False,
    json: bool = False,
) -> int:
    process = run(
        [
            sys.executable,
            "-m",
            "conda",
            "install",
            f"--prefix={sys.prefix}",
            *(
                ("--override-frozen",)
                if hasattr(context, "protect_frozen_envs")
                else ()
            ),
            *(("--force-reinstall",) if force_reinstall else ()),
            *(("--json",) if json else ()),
            "--update-specs",
            "--override-channels",
            f"--channel={channel}",
            f"{package_name}={package_version}",
        ]
    )
    return process.returncode


def install_specs_in_protected_env(
    specs: list[str],
    channel: str = None,
    force_reinstall: bool = False,
    json: bool = False,
    yes: bool = True,
) -> int:
    cmd = [
            sys.executable,
            "-m",
            "conda",
            "install",
            f"--prefix={sys.prefix}",
            *(
                ("--override-frozen",)
                if hasattr(context, "protect_frozen_envs")
                else ()
            ),
            *(("--force-reinstall",) if force_reinstall else ()),
            *(("--json",) if json else ()),
            "--override-channels",
            *((f"--channel={channel}") if channel is not None else (f"--channel={chn}" for chn in context.channels)),
            *(("--yes",) if yes else ()),
            *specs
        ]
    process = run(cmd)
    return process.returncode


def uninstall_specs_in_protected_env(
    specs: list[str],
    json: bool = False,
    yes: bool = True,
) -> int:
    cmd = [
            sys.executable,
            "-m",
            "conda",
            "remove",
            f"--prefix={sys.prefix}",
            *(
                ("--override-frozen",)
                if hasattr(context, "protect_frozen_envs")
                else ()
            ),
            *(("--json",) if json else ()),
            *(("--yes",) if yes else ()),
            *specs
        ]
    process = run(cmd)
    return process.returncode