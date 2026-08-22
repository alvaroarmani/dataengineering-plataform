"""Testes do Exercício 04 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import receita_por_categoria  # noqa: E402


def _registros(df):
    return df.to_dict("records")


def test_agrega_e_ordena():
    # livros=80, eletronicos=1200, casa=80. Ordena por receita desc;
    # no empate (80), a ordem do groupby (alfabética) mantém 'casa' antes de 'livros'.
    df = pd.DataFrame({
        "categoria": ["livros", "eletronicos", "livros", "casa"],
        "valor": [50.0, 1200.0, 30.0, 80.0],
    })
    assert _registros(receita_por_categoria(df)) == [
        {"categoria": "eletronicos", "receita": 1200.0},
        {"categoria": "casa", "receita": 80.0},
        {"categoria": "livros", "receita": 80.0},
    ]


def test_ignora_nan():
    df = pd.DataFrame({"categoria": ["a", "b", "a"], "valor": [10.0, np.nan, 5.0]})
    assert _registros(receita_por_categoria(df)) == [{"categoria": "a", "receita": 15.0}]


def test_colunas_e_indice():
    df = pd.DataFrame({"categoria": ["a", "b"], "valor": [1.0, 2.0]})
    out = receita_por_categoria(df)
    assert list(out.columns) == ["categoria", "receita"]
    assert list(out.index) == [0, 1]  # índice reiniciado


def test_vazio():
    df = pd.DataFrame({"categoria": [], "valor": []})
    out = receita_por_categoria(df)
    assert list(out.columns) == ["categoria", "receita"]
    assert len(out) == 0
