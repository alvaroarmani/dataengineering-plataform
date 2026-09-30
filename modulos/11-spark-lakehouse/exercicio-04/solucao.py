"""Exercício 04 (M11) — Pipeline imutável de transformações.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def aplicar(linhas: list, passos: list) -> list:
    """passos (em ordem):
      ("withColumn", nome, func)  func(linha) -> valor; cria ou SOBRESCREVE a coluna
      ("filter", func)            mantém as linhas com func(linha) verdadeiro
      ("drop", nome)              remove a coluna (inexistente -> ValueError)
    Nunca altere `linhas` nem os dicts dentro dela: cada passo trabalha com cópias.
    Se uma func acessar coluna inexistente (KeyError), levante ValueError com o índice do passo."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
