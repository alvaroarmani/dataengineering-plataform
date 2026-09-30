import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import construir_grafo, vizinhos  # noqa: E402

SEGUE = [("ana", "bruno"), ("bruno", "ana"), ("ana", "caio"), ("ana", "caio"),
         ("caio", "caio"), ("dara", "ana")]


def test_nao_dirigido():
    assert construir_grafo(SEGUE) == {
        "ana": ["bruno", "caio", "dara"], "bruno": ["ana"], "caio": ["ana"], "dara": ["ana"]}


def test_dirigido():
    assert construir_grafo(SEGUE, dirigido=True) == {
        "ana": ["bruno", "caio"], "bruno": ["ana"], "caio": [], "dara": ["ana"]}


def test_laco_isolado_ainda_cria_o_no():
    assert construir_grafo([("x", "x")]) == {"x": []}


def test_vizinhos():
    g = construir_grafo(SEGUE, dirigido=True)
    assert vizinhos(g, "ana") == ["bruno", "caio"]
    assert vizinhos(g, "caio") == []
    with pytest.raises(KeyError):
        vizinhos(g, "zeca")


def test_no_nulo():
    with pytest.raises(ValueError):
        construir_grafo([("ana", None)])


def test_vazio():
    assert construir_grafo([]) == {}
