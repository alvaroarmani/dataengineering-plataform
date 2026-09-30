"""Exercício 10 (M8) — Schema drift na borda: aceitar, avisar ou rejeitar.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""


PROMOCOES = {("float", "int")}   # (esperado, recebido) que se pode alargar sem perda


def conciliar_schema(esperado: dict, registro: dict) -> dict:
    """esperado = {coluna: {"tipo": "int"|"float"|"str"|"bool", "nulo": bool}} (todas obrigatórias).
    Retorne {"decisao": "aceitar"|"aceitar_com_aviso"|"rejeitar",
             "faltando": [...], "extras": [...], "incompativeis": [...], "promovidas": [...]} (listas ordenadas):
      faltando       coluna do contrato ausente no registro                      -> rejeita
      incompativeis  tipo diferente e não promovível, ou None onde "nulo" é False -> rejeita
      promovidas     int recebido onde se espera float                           -> aviso
      extras         coluna fora do contrato                                     -> aviso
    bool NUNCA é aceito como int/float (em Python, True é int)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
