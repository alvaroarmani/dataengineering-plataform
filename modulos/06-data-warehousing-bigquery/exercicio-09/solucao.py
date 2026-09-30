"""Exercício 09 (M6) — Bytes varridos: poda de coluna x poda de partição.

Rode `pytest -q`. Detalhes no enunciado (exercicio-09.md).
"""


def bytes_varridos(tabela: dict, consulta: dict) -> int:
    """tabela = {"bytes_por_coluna": {col: bytes da coluna na tabela inteira}, "particoes": n,
                 "coluna_particao": col}
    consulta = {"colunas": [cols lidas] ou ["*"], "filtro_particao": {"coluna": col, "particoes": k} ou None}
    Bytes = soma dos bytes das colunas lidas * fração de partições lidas, onde:
      - "*" lê todas as colunas;
      - a fração é k / particoes SÓ se o filtro é na coluna_particao; senão (ou sem filtro) é 1;
    Resultado inteiro (arredonde para baixo). Coluna inexistente, k fora de 1..particoes -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def economia_pct(tabela: dict, consulta: dict) -> float:
    """Economia (%) em relação a um SELECT * sem filtro, 1 casa."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
