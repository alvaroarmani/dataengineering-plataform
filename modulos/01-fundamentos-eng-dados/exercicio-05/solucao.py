"""Exercício 05 (M1) — Linha x coluna: quantos bytes a consulta lê.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def bytes_lidos(tabela: dict, colunas_da_consulta: list, formato: str) -> int:
    """tabela = {"linhas": n, "colunas": {nome: {"bytes": bytes por valor, "compressao": fator}}}.
      "linha":  lê TODAS as colunas, sem compressão: linhas * soma(bytes de todas)
      "coluna": lê só as colunas da consulta, cada uma comprimida: soma(linhas * bytes / compressao)
    Resultado inteiro (arredonde para baixo). Coluna inexistente ou formato desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def ganho(tabela: dict, colunas_da_consulta: list) -> float:
    """Quantas vezes o formato por linha lê mais que o colunar (1 casa)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
