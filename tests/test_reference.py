"""Determinism and argument-contract checks for the new portable CPU reference."""
from __future__ import annotations
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINARY = ROOT / "matmul_reference"


def run(n: str):
    return subprocess.run([str(BINARY), n], text=True, capture_output=True)


def test_supported_sizes_and_deterministic_checksum():
    for size in (1, 8, 16, 64):
        first = run(str(size))
        second = run(str(size))
        assert first.returncode == 0, first.stderr
        assert second.returncode == 0, second.stderr
        for output in (first.stdout, second.stdout):
            assert f"n={size} " in output
            assert "reference=cpu-naive" in output
        checksum = lambda output: float(re.search(r"checksum=([-0-9.]+)", output).group(1))
        assert checksum(first.stdout) == checksum(second.stdout)


def test_invalid_size_is_rejected():
    for value in ("0", "513", "bad", "-1", "4x"):
        p = run(value)
        assert p.returncode == 2
        assert "usage" in p.stderr
