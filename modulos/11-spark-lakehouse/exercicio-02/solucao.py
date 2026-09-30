"""Exercício 02 (M11) — Catalyst: column pruning e predicate pushdown.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


def otimizar(plano: list, colunas_fonte: list) -> dict:
    """plano = lista de passos, em ordem:
      ("withColumn", nova, [colunas usadas])   ("filter", [colunas usadas])   ("select", [colunas])
    O resultado final são as colunas do ÚLTIMO select (se não houver select, todas as disponíveis).
    Retorne {"colunas_lidas": colunas da fonte realmente necessárias (ordenadas),
             "filtros_empurrados": índices dos filtros que usam SÓ colunas da fonte}.
    Referência a coluna inexistente no ponto em que aparece -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
