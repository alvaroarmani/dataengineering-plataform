"""Testes do Exercício 08 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import estado_do_run  # noqa: E402


def test_run_com_falha():
    tasks = [("a", "success"), ("b", "failed"), ("c", "success")]
    assert estado_do_run(tasks) == {"success": 2, "failed": 1, "skipped": 0, "run_ok": False}


def test_run_ok():
    tasks = [("a", "success"), ("b", "success")]
    assert estado_do_run(tasks) == {"success": 2, "failed": 0, "skipped": 0, "run_ok": True}


def test_com_skipped():
    tasks = [("a", "success"), ("b", "skipped")]
    assert estado_do_run(tasks) == {"success": 1, "failed": 0, "skipped": 1, "run_ok": True}
