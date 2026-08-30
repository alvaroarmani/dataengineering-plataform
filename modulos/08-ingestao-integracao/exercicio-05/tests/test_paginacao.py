"""Testes do Exercício 05 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import coletar_tudo  # noqa: E402


def test_coleta_todas_as_paginas():
    paginas = {1: [1, 2], 2: [3, 4], 3: [5], 4: []}
    assert coletar_tudo(lambda n: paginas.get(n, [])) == [1, 2, 3, 4, 5]


def test_primeira_pagina_vazia():
    assert coletar_tudo(lambda n: []) == []


def test_para_na_primeira_vazia():
    # deve parar assim que uma página vem vazia (não pular buracos)
    chamadas = []

    def buscar(n):
        chamadas.append(n)
        return {1: ["a"], 2: [], 3: ["b"]}.get(n, [])

    assert coletar_tudo(buscar) == ["a"]
    assert chamadas == [1, 2]  # parou na página 2 (vazia)
