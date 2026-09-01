"""Testes do Projeto Integrador do Eixo 3. Faça todos passarem: pytest -q"""
import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from pipeline import parse_cotacoes, upsert_idempotente, checar_qualidade  # noqa: E402


def _payload():
    return json.loads((RAIZ / "data" / "amostra_api.json").read_text(encoding="utf-8"))


def test_parse_ordena_e_extrai_data():
    df = parse_cotacoes(_payload())
    assert list(df.columns) == ["data", "valor"]
    assert df.to_dict("records") == [
        {"data": "2026-08-09", "valor": 4.98},
        {"data": "2026-08-10", "valor": 5.01},
        {"data": "2026-08-11", "valor": 5.03},
    ]


def test_upsert_idempotente_e_overwrite():
    destino = pd.DataFrame({"data": ["2026-08-09", "2026-08-10"], "valor": [4.98, 5.01]})
    novos = pd.DataFrame({"data": ["2026-08-10", "2026-08-11"], "valor": [5.99, 5.03]})  # 10 muda
    r1 = upsert_idempotente(destino, novos)
    assert r1.to_dict("records") == [
        {"data": "2026-08-09", "valor": 4.98},
        {"data": "2026-08-10", "valor": 5.99},   # overwrite pelo valor novo
        {"data": "2026-08-11", "valor": 5.03},
    ]
    # idempotência: aplicar de novo os mesmos `novos` não muda o resultado
    r2 = upsert_idempotente(r1, novos)
    assert r2.to_dict("records") == r1.to_dict("records")


def test_qualidade_detecta_problemas():
    ruim = pd.DataFrame({"data": ["2026-08-09", "2026-08-09"], "valor": [-1.0, 5.0]})
    assert checar_qualidade(ruim) == ["data_duplicada", "valor_negativo"]
    bom = pd.DataFrame({"data": ["2026-08-09"], "valor": [5.0]})
    assert checar_qualidade(bom) == []
