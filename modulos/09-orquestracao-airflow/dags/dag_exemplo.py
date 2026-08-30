"""DAG de exemplo do M09 — roda na bancada (profile airflow).

Montada em /opt/airflow/dags pelo docker-compose. Rode:
  docker compose --profile airflow up -d
  docker compose exec airflow airflow dags test pipeline_exemplo 2026-01-01
"""
import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="pipeline_exemplo",
    start_date=dt.datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["curso", "m09"],
) as dag:
    extrair = BashOperator(task_id="extrair", bash_command="echo 'extraindo...'")
    carregar = BashOperator(task_id="carregar", bash_command="echo 'carregando...'")
    transformar = BashOperator(task_id="transformar", bash_command="echo 'transformando...'")
    validar = BashOperator(task_id="validar", bash_command="echo 'validando...'")

    # Dependências: cada task depende da anterior (roda em ordem).
    extrair >> carregar >> transformar >> validar
