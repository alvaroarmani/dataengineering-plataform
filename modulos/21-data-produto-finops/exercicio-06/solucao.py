"""Exercício 06 (M21) — Scorecard de um data product (DATSIS).

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


REQUISITOS = ["dono", "descricao", "sla", "schema_documentado", "testes_passando", "pii_classificada"]


def avaliar_produto(produto: dict) -> dict:
    """produto = {"dono": str, "descricao": str, "sla": {"freshness_horas": n},
                  "colunas": [{"nome", "descricao", "pii": True|False}], "testes": {nome: passou}}
    Pendências (nomes de REQUISITOS):
      dono               texto não vazio (espaços não contam)
      descricao          ao menos 20 caracteres (após strip)
      sla                "freshness_horas" numérico > 0
      schema_documentado há colunas e TODAS têm descrição não vazia
      testes_passando    há ao menos um teste e TODOS passaram
      pii_classificada   há colunas e TODAS têm "pii" explicitamente True ou False
    Retorne {"pronto": bool, "pendencias": [ordenadas], "nota": % de requisitos atendidos, 1 casa}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
