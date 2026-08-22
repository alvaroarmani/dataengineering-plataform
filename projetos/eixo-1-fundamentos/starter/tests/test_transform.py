"""Testes da transformação. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.transform import adicionar_receita, limpar, padronizar_estado  # noqa: E402


def test_padronizar_estado():
    df = pd.DataFrame({"estado": ["sp", "RJ", "mg"]})
    assert list(padronizar_estado(df)["estado"]) == ["SP", "RJ", "MG"]


def test_limpar_remove_invalidos():
    df = pd.DataFrame({"valor": ["100", "", "abc", "50"], "quantidade": [1, 1, 1, 2]})
    out = limpar(df)
    assert list(out["valor"]) == [100.0, 50.0]  # remove vazio e 'abc', converte para float


def test_adicionar_receita():
    df = pd.DataFrame({"valor": [10.0, 5.0], "quantidade": [2, 3]})
    out = adicionar_receita(df)
    assert list(out["receita"]) == [20.0, 15.0]


def test_transform_nao_muta_original():
    df = pd.DataFrame({"estado": ["sp"]})
    padronizar_estado(df)
    assert df.loc[0, "estado"] == "sp"  # a função deve retornar cópia, não mutar
