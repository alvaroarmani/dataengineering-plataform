"""Testes do Exercício 06 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import carregar_dia  # noqa: E402

ESPERADO = [
    ("2026-08-09", 1, 10),
    ("2026-08-10", 2, 20),
    ("2026-08-10", 3, 30),
]


def test_overwrite_do_dia():
    fato = [("2026-08-09", 1, 10), ("2026-08-10", 9, 99)]  # dado velho do dia 10
    batch = [(2, 20), (3, 30)]
    assert carregar_dia(fato, "2026-08-10", batch) == ESPERADO


def test_idempotente_rodar_2x():
    fato = [("2026-08-09", 1, 10)]
    batch = [(2, 20), (3, 30)]
    r1 = carregar_dia(fato, "2026-08-10", batch)
    r2 = carregar_dia(r1, "2026-08-10", batch)  # reprocessa: não pode duplicar
    assert r1 == r2 == ESPERADO
