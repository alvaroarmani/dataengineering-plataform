"""Exercício 06 (M14) — Direito ao esquecimento em várias tabelas.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

import copy


def esquecer_titular(tabelas: dict, titular_id, politica: dict) -> tuple:
    """tabelas = {nome: [registros]}, todo registro tem "cliente_id".
    politica = {nome: {"acao": "apagar"|"anonimizar"|"manter", "campos": [campos pessoais]}}.
      apagar     -> remove os registros do titular
      anonimizar -> nos registros do titular, cada campo de "campos" que existir vira "***"
                    e "cliente_id" vira None (o vínculo com a pessoa é o próprio dado pessoal)
      manter     -> não altera nada (retenção legal)
    Não altere a entrada: devolva (novas_tabelas, relatorio) com relatorio = {nome: {"acao", "registros"}}
    (registros = quantos registros do titular havia na tabela).
    Tabela sem política -> ValueError (nada de esquecimento pela metade)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
