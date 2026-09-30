import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import validar_escrita  # noqa: E402

TABELA = {"id": {"tipo": "long", "nulo": False}, "valor": {"tipo": "double", "nulo": False},
          "cupom": {"tipo": "string", "nulo": True}}


def test_escrita_compativel():
    r = validar_escrita(TABELA, {"id": "long", "valor": "double", "cupom": "string"})
    assert r["aceita"] is True and r["schema_final"] == TABELA


def test_coluna_nova_sem_e_com_merge_schema():
    df = {"id": "long", "valor": "double", "canal": "string"}
    assert validar_escrita(TABELA, df)["motivos"] == ["nova:canal"]
    r = validar_escrita(TABELA, df, merge_schema=True)
    assert r["aceita"] is True and r["schema_final"]["canal"] == {"tipo": "string", "nulo": True}


def test_tipo_mais_estreito_entra_mais_largo_nao():
    assert validar_escrita(TABELA, {"id": "int", "valor": "float"})["aceita"] is True
    assert validar_escrita({"n": {"tipo": "int", "nulo": False}}, {"n": "long"})["motivos"] == ["tipo:n"]


def test_mudanca_de_tipo_recusada_mesmo_com_merge():
    r = validar_escrita(TABELA, {"id": "long", "valor": "string"}, merge_schema=True)
    assert r == {"aceita": False, "motivos": ["tipo:valor"], "schema_final": TABELA}


def test_obrigatoria_ausente():
    assert validar_escrita(TABELA, {"id": "long"})["motivos"] == ["obrigatoria:valor"]
