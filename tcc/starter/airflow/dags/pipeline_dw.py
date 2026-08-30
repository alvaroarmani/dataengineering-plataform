"""DAG do pipeline do DW: ingestão -> dbt build. Agendada e idempotente (Etapa 4).

TODO: ajuste os comandos ao seu ambiente (caminhos, container dbt vs local).
Valide sem scheduler:  airflow dags test pipeline_dw 2024-01-01
"""
from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="pipeline_dw",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,             # comece sem backfill
    default_args={"retries": 2},
    tags=["tcc", "dw"],
) as dag:

    ingestao_raw = BashOperator(
        task_id="ingestao_raw",
        # idempotente: o script recria as tabelas raw (if_exists='replace')
        bash_command="python /opt/airflow/dags/../../ingestao/carregar_olist.py",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        # roda models + testes; falha a DAG se algum teste quebrar
        bash_command="cd /opt/dbt && dbt build",
    )

    ingestao_raw >> dbt_build
