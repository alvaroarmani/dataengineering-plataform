"""Trilha real (bancada) — DAG Airflow do ELT de câmbio, idempotente e agendada.

Valide sem scheduler:  airflow dags test dag_cambio 2026-08-10
TODO: complete as tasks reaproveitando as funções puras de ../pipeline.py.
"""
from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _extrair(**_):
    # TODO: requests.get da API do Banco Central -> payload; parse_cotacoes(payload)
    ...


def _carregar(**_):
    # TODO: upsert_idempotente no destino (Postgres/arquivo) — reprocessar não duplica
    ...


def _qualidade(**_):
    # TODO: checar_qualidade(df); falhe a task se houver problemas
    ...


with DAG(
    dag_id="dag_cambio",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2},
    tags=["eixo3", "elt"],
) as dag:
    extrair = PythonOperator(task_id="extrair", python_callable=_extrair)
    carregar = PythonOperator(task_id="carregar", python_callable=_carregar)
    qualidade = PythonOperator(task_id="qualidade", python_callable=_qualidade)
    extrair >> carregar >> qualidade
