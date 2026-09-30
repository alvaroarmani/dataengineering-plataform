"""Exercício 02 (M13) — Branch → ambiente e schema de deploy.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

import re
import unicodedata


def alvo_de_deploy(branch: str, usuario: str) -> dict:
    """Retorne {"ambiente": ..., "schema": ...}:
      "main"                      -> prod,    "analytics"
      "develop"                   -> staging, "analytics_staging"
      "feature/<x>" ou "fix/<x>"  -> dev,     "dev_<usuario>_<x>"
    Normalização de <usuario> e <x>: sem acentos, minúsculas, qualquer sequência de caracteres que não
    seja letra/dígito vira "_", sem "_" nas pontas; <x> limitado a 30 caracteres (sem "_" final).
    Outro padrão de branch, <x> vazio após normalizar, ou usuário vazio -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
