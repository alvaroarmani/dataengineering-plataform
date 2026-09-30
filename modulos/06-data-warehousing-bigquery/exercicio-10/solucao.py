"""Exercício 10 (M6) — Layout físico a partir do workload.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""


PARTICIONAVEIS = {"date", "timestamp", "int"}


def layout_recomendado(consultas: list, tipos: dict) -> dict:
    """consultas = [(colunas_filtradas, execucoes_por_dia)]; tipos = {coluna: tipo}.
    Peso de uma coluna = soma das execuções das consultas que a filtram.
      particao: a coluna PARTICIONÁVEL (tipo em PARTICIONAVEIS) de maior peso (empate: nome), ou None;
      cluster:  até 4 colunas de maior peso, sem a coluna de partição, em ordem de peso (empate: nome).
    Coluna sem tipo conhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
