"""Exercício 06 (M3) — Validação de registro (checagem de qualidade).

Implemente `validar_registro` e rode `pytest -q` nesta pasta até tudo passar.
"""

ESTADOS_OK = {"SP", "RJ", "MG"}


def validar_registro(reg):
    """Recebe um dicionário e retorna a lista de erros (vazia se válido), na ordem:
    1) "id ausente"        se falta a chave 'id'
    2) "valor ausente"     se falta 'valor'
    3) "valor negativo"    se 'valor' existe e é < 0
    4) "estado inválido"   se 'estado' existe e não está em {SP, RJ, MG}
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
