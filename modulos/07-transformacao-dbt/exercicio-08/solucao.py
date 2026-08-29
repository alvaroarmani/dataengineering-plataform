"""Exercício 08 (M7) — Macros: transformações reutilizáveis (a ideia por trás do Jinja).

Um macro dbt encapsula um trecho de SQL reutilizável. Aqui, em Python, implemente dois
"macros" clássicos e rode `pytest -q`.
"""


def centavos_para_reais(centavos):
    """Converte um valor em centavos (int) para reais (float): 12345 -> 123.45."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def surrogate_key(valores):
    """Gera uma surrogate key DETERMINÍSTICA a partir de uma lista de valores
    (como dbt_utils.generate_surrogate_key): mesmo input -> mesma chave; inputs
    diferentes -> chaves diferentes. Retorne uma string (ex.: hash hexadecimal)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
