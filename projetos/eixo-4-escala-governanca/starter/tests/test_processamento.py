"""Testes do Projeto Integrador do Eixo 4. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from processamento import transformar, agregar_por_dia, escrever_parquet  # noqa: E402


def _dados():
    return pd.read_csv(RAIZ / "data" / "amostra_corridas.csv")


def test_transformar_limpa_e_deriva():
    out = transformar(_dados())
    assert list(out.columns) == ["data", "passageiros", "valor", "duracao_min"]
    assert out.to_dict("records") == [
        {"data": "2026-01-01", "passageiros": 1, "valor": 20.0, "duracao_min": 15.0},
        {"data": "2026-01-01", "passageiros": 2, "valor": 40.0, "duracao_min": 30.0},
        {"data": "2026-01-02", "passageiros": 1, "valor": 12.0, "duracao_min": 10.0},
    ]  # remove duração negativa e passageiros=0


def test_agregar_por_dia():
    agg = agregar_por_dia(transformar(_dados()))
    assert agg.to_dict("records") == [
        {"data": "2026-01-01", "corridas": 2, "receita": 60.0, "duracao_media": 22.5},
        {"data": "2026-01-02", "corridas": 1, "receita": 12.0, "duracao_media": 10.0},
    ]


def test_escrever_e_ler_parquet(tmp_path):
    agg = agregar_por_dia(transformar(_dados()))
    caminho = tmp_path / "corridas.parquet"
    escrever_parquet(agg, str(caminho))
    assert caminho.exists()
    lido = pd.read_parquet(caminho)
    assert lido.to_dict("records") == agg.to_dict("records")
