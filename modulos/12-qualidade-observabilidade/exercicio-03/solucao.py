"""Exercício 03 (M12) — Unicidade com chave composta.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def checar_unicidade(linhas: list, chave: list) -> dict:
    """`chave` é a lista de campos que deveria identificar cada linha.

    Retorne:
      {"duplicadas": [(valores_da_chave, ocorrencias), ...],   # só chaves com ocorrencias > 1,
                                                               # ordenadas por ocorrencias desc e chave
       "chave_incompleta": n}                                  # linhas com algum componente None/ausente
    Linhas com chave incompleta NÃO entram na contagem de duplicadas.
    `valores_da_chave` é uma tupla na ordem de `chave`. Chave vazia -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
