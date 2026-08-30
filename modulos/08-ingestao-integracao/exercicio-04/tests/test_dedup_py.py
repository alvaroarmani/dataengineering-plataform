"""Testes do Exercício 04 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import dedup  # noqa: E402


def test_dedup_mais_recente():
    linhas = [
        (1, 100, "2026-08-10"),
        (2, 200, "2026-08-10"),
        (3, 300, "2026-08-11"),
        (1, 150, "2026-08-12"),
    ]
    assert dedup(linhas) == [(1, 150), (2, 200), (3, 300)]


def test_dedup_sem_duplicatas():
    linhas = [(5, 50, "2026-01-01"), (6, 60, "2026-01-02")]
    assert dedup(linhas) == [(5, 50), (6, 60)]


def test_dedup_vazio():
    assert dedup([]) == []
