"""DAG TaskFlow do M09 — @task + XCom (o retorno de uma task vira XCom da próxima).

Rode na bancada:
  docker compose exec airflow airflow dags test pipeline_taskflow 2026-01-01
"""
import datetime as dt

from airflow.decorators import dag, task


@dag(
    dag_id="pipeline_taskflow",
    start_date=dt.datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["curso", "m09"],
)
def pipeline_taskflow():
    @task
    def extrair():
        return [1, 2, 3, 4]

    @task
    def somar(nums):
        return sum(nums)

    @task
    def reportar(total):
        print(f"total = {total}")

    # Dependências inferidas pela passagem de valores (XCom implícito):
    reportar(somar(extrair()))


pipeline_taskflow()
