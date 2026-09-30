"""Exercício 10 (M9) — Data-aware scheduling: DAGs disparadas por datasets.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""


def disparos(consumidores: dict, atualizacoes: list) -> list:
    """consumidores = {dag: [datasets de que depende]}; atualizacoes = [dataset atualizado] em ordem.
    Após cada atualização, toda DAG cujos datasets TODOS foram atualizados desde o último disparo dela
    é disparada (e o controle dela zera). Retorne [(indice_da_atualizacao, dag)] em ordem de índice e,
    no mesmo índice, ordem alfabética. DAG sem datasets -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
