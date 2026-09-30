import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import revisar_design  # noqa: E402

SO_CAIXAS = """
Os eventos do app vão para o Kafka. Um job Spark lê o tópico, agrega por minuto e grava no BigQuery.
O dashboard no Looker lê a tabela agregada. O catálogo de dados é o Dataplex.
"""

COMPLETO = """
Eventos vão para o Kafka e o Spark grava no BigQuery com MERGE por chave, então o job é idempotente e
podemos reprocessar qualquer dia. Testes do dbt validam unicidade; alertas de freshness vão para o Slack.
Acesso por IAM com mascaramento do e-mail (LGPD). A tabela é particionada por dia para controlar o custo.
"""


def test_so_caixas():
    r = revisar_design(SO_CAIXAS)
    assert r["cobertas"] == []
    assert r["faltando"] == ["qualidade", "seguranca", "observabilidade", "custo", "idempotencia"]
    assert r["perguntas"][0] == "Como você garante que o dado que chega está correto?"


def test_design_completo():
    assert revisar_design(COMPLETO) == {
        "cobertas": ["qualidade", "seguranca", "observabilidade", "custo", "idempotencia"],
        "faltando": [], "perguntas": []}


def test_acentos_e_inicio_de_palavra():
    r = revisar_design("Validação por contrato. Pipeline idempotente. Observabilidade com métricas.")
    assert r["faltando"] == ["seguranca", "custo"]


def test_palavra_dentro_de_outra_nao_conta():
    assert "observabilidade" in revisar_design("Registramos tudo no catálogo e no dialogo com o time.")["faltando"]
