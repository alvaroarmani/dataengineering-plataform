"""Exercício 08 (M11) — Schema enforcement x schema evolution no Delta.

Rode `pytest -q`. Detalhes no enunciado (exercicio-08.md).
"""


ALARGAMENTOS = {("int", "long"), ("float", "double"), ("int", "double")}


def validar_escrita(tabela: dict, df: dict, merge_schema: bool = False) -> dict:
    """tabela = {coluna: {"tipo", "nulo"}}; df = {coluna: tipo} (schema do DataFrame a gravar).
    Regras, nesta ordem:
      1. coluna em ambos com tipo diferente: aceita só se (tipo_df, tipo_tabela) está em ALARGAMENTOS
         (o DataFrame traz um tipo MAIS ESTREITO, que cabe na coluna: df int -> tabela long);
         qualquer outra diferença -> recusa "tipo:<col>"
      2. coluna da tabela ausente no df: aceita se "nulo" for True; senão recusa "obrigatoria:<col>"
      3. coluna nova no df: com merge_schema, entra no schema (anulável); sem -> recusa "nova:<col>"
    Retorne {"aceita": bool, "motivos": [ordenados], "schema_final": dict da tabela (atualizado se aceita)}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
