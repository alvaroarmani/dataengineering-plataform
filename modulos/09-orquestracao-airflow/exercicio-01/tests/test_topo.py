"""Testes do Exercício 01 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import ordem_topologica  # noqa: E402

TASKS = ["extrair", "carregar", "validar", "transformar"]
ARESTAS = [
    ("extrair", "carregar"),
    ("extrair", "validar"),
    ("carregar", "transformar"),
    ("validar", "transformar"),
]


def _valida(ordem, tasks, arestas):
    assert sorted(ordem) == sorted(tasks), "deve conter todas as tasks, sem repetir"
    pos = {t: i for i, t in enumerate(ordem)}
    for a, b in arestas:
        assert pos[a] < pos[b], f"{a} deve vir antes de {b}"


def test_ordem_respeita_dependencias():
    _valida(ordem_topologica(TASKS, ARESTAS), TASKS, ARESTAS)


def test_cadeia_linear():
    tasks = ["a", "b", "c"]
    arestas = [("a", "b"), ("b", "c")]
    assert ordem_topologica(tasks, arestas) == ["a", "b", "c"]


def test_sem_dependencias():
    ordem = ordem_topologica(["x", "y"], [])
    assert sorted(ordem) == ["x", "y"]
