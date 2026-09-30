"""Exercício 02 (M22) — Grau de entrada e saída: fontes e sumidouros do lineage.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


def graus(lineage: dict) -> dict:
    """lineage = {tabela: [tabelas que ela ALIMENTA]} (aresta tabela -> consumidor).
    Retorne {no: (grau_entrada, grau_saida)} para TODOS os nós, inclusive os que só aparecem
    como destino. Destinos repetidos na mesma lista contam uma vez."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fontes_e_sumidouros(lineage: dict) -> dict:
    """{"fontes": [grau de entrada 0], "sumidouros": [grau de saída 0],
        "mais_dependida": nó de MAIOR grau de saída (empate: ordem alfabética)}.
    Um nó isolado (0 e 0) é fonte E sumidouro. Lineage vazio -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
