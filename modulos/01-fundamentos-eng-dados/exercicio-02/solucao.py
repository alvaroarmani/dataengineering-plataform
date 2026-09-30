"""Exercício 02 (M1) — OLTP ou OLAP? Classificando pela carga real.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

from statistics import median


def perfil_carga(consultas: list) -> dict:
    """consultas = [{"tipo": "SELECT"|"INSERT"|"UPDATE"|"DELETE", "linhas_lidas": int, "agrega": bool}].
    Métricas (2 casas nas frações):
      pct_escrita    = fração de INSERT/UPDATE/DELETE
      pct_agregacao  = fração de consultas com agrega=True
      mediana_lidas  = mediana de linhas_lidas (statistics.median)
    Classe:
      "OLTP" se pct_escrita >= 0.3 e mediana_lidas <= 100
      "OLAP" se pct_agregacao >= 0.5 ou mediana_lidas >= 10_000
      senão "misto"
    (teste OLTP primeiro). Lista vazia ou tipo desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
