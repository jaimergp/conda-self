import sys

from conda.core.prefix_data import PrefixData


def test_help(conda_cli):
    out, err, exc = conda_cli("self", "reset", "--help", raises=SystemExit)
    assert exc.value.code == 0


def test_reset(conda_cli, tmp_path):
    tmp_prefix = sys.prefix

    assert len(tuple(PrefixData(tmp_prefix).query("numpy"))) == 0

    conda_cli("install", "numpy", "--yes")

    assert len(tuple(PrefixData(tmp_prefix).query("numpy"))) == 1

    conda_cli(
        "self",
        "reset",
    )

    assert len(tuple(PrefixData(tmp_prefix).query("numpy"))) == 0
