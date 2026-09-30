"""Exercício 05 (M10) — Interpolação de variáveis do Compose.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""

import re

PADRAO = re.compile(r"\$\$|\$\{(?P<nome>[A-Za-z_][A-Za-z0-9_]*)(?:(?P<op>:-|-|:\?|\?)(?P<arg>[^}]*))?\}|\$(?P<simples>[A-Za-z_][A-Za-z0-9_]*)")


def interpolar(texto: str, ambiente: dict) -> str:
    """Substitua no texto:
      $$              -> $
      $VAR, ${VAR}    -> valor (ausente -> "")
      ${VAR:-p}       -> p se VAR ausente OU vazia;       ${VAR-p}  -> p só se ausente
      ${VAR:?msg}     -> ValueError(msg) se ausente OU vazia; ${VAR?msg} -> só se ausente
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
