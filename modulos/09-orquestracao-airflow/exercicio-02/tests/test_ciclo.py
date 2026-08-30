"""Testes do Exercício 02 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import tem_ciclo  # noqa: E402


def test_dag_valida_sem_ciclo():
    tasks = ["a", "b", "c", "d"]
    arestas = [("a", "b"), ("b", "c"), ("b", "d")]
    assert tem_ciclo(tasks, arestas) is False


def test_ciclo_simples():
    tasks = ["a", "b"]
    arestas = [("a", "b"), ("b", "a")]
    assert tem_ciclo(tasks, arestas) is True


def test_ciclo_maior():
    tasks = ["a", "b", "c"]
    arestas = [("a", "b"), ("b", "c"), ("c", "a")]
    assert tem_ciclo(tasks, arestas) is True


def test_sem_arestas():
    assert tem_ciclo(["x", "y"], []) is False
