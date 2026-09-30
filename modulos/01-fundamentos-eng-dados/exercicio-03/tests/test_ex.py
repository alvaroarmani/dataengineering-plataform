import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import validar_pipeline  # noqa: E402

BOM = [("app grava pedido", "geracao"), ("extrai com Airbyte", "ingestao"), ("salva no lake", "armazenamento"),
       ("dbt staging", "transformacao"), ("dbt marts", "transformacao"), ("dashboard", "disponibilizacao")]


def test_pipeline_ok():
    r = validar_pipeline(BOM)
    assert r["ok"] is True and r["fora_de_ordem"] == [] and r["fases_ausentes"] == []


def test_etapa_fora_de_ordem():
    etapas = [("extrai", "ingestao"), ("limpa no script de extração", "transformacao"),
              ("salva no lake", "armazenamento"), ("dashboard", "disponibilizacao")]
    r = validar_pipeline(etapas)
    assert r["fora_de_ordem"] == ["salva no lake"]
    assert r["ordem_correta"] == ["extrai", "salva no lake", "limpa no script de extração", "dashboard"]
    assert r["ok"] is False


def test_fase_ausente_dashboard_lendo_da_fonte():
    r = validar_pipeline([("app grava", "geracao"), ("dashboard", "disponibilizacao")])
    assert r["fases_ausentes"] == ["ingestao", "armazenamento", "transformacao"]


def test_ordem_estavel_dentro_da_fase():
    r = validar_pipeline([("marts", "transformacao"), ("staging", "transformacao"), ("ingere", "ingestao")])
    assert r["ordem_correta"] == ["ingere", "marts", "staging"]


def test_corrente_de_fundo_nao_e_fase():
    with pytest.raises(ValueError, match="corrente de fundo"):
        validar_pipeline([("airflow", "orquestracao")])
    with pytest.raises(ValueError):
        validar_pipeline([("x", "limpeza")])
