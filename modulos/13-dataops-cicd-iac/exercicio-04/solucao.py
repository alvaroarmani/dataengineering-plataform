"""Exercício 04 (M13) — Slim CI: o que o dbt precisa rebuildar.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def selecao_slim_ci(arquivos_mudados: list, dag: dict) -> list:
    """dag = {modelo: [modelos que dependem dele]} (todos os modelos são chaves).
    Regras, a partir dos caminhos alterados:
      - "models/.../<nome>.sql" -> o modelo <nome> mudou (nome fora do dag -> ValueError)
      - qualquer arquivo em "macros/" -> TODOS os modelos
      - "dbt_project.yml" -> TODOS os modelos
      - o resto (.md, .yml de docs, README...) não seleciona nada
    Retorne a lista ORDENADA dos modelos mudados + todos os descendentes (transitivos)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
