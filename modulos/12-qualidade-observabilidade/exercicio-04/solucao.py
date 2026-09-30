"""Exercício 04 (M12) — Validade: domínio e normalização.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def relatorio_dominio(valores: list, permitidos: list) -> dict:
    """Classifique cada valor e retorne:
      {"validos": n,              # exatamente igual a um permitido
       "corrigiveis": {v: n},     # vira permitido após strip() + lower()  (chave = valor original)
       "invalidos": {v: n},       # nem assim (None também é inválido)
       "pct_invalido": x}         # % de inválidos sobre o total, 2 casas (0.0 se a lista for vazia)
    Os permitidos são comparados já normalizados (strip + lower).
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
