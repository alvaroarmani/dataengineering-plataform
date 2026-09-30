"""Exercício 10 (M11) — Dimensionar partições e evitar arquivos pequenos.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""

import math


def planejar_particoes(tamanho_mb: float, cores: int, alvo_mb: float = 128) -> dict:
    """n = ceil(tamanho / alvo), no mínimo `cores`, arredondado PARA CIMA ao múltiplo de `cores`.
    Retorne {"particoes": n, "mb_por_particao": tamanho / n com 1 casa, "ondas": n // cores}.
    cores < 1 ou alvo <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def arquivos_gravados(datas_por_tarefa: list, repartition_por_data: bool) -> int:
    """datas_por_tarefa = para cada tarefa (partição) do DataFrame, o conjunto de datas que ela contém.
    Sem repartition: cada tarefa grava 1 arquivo por data distinta que contém.
    Com repartition por data: 1 arquivo por data distinta no total."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
