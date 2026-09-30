"""Exercício 04 (M19) — Eleição no Raft: quem pode receber o voto.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def log_ok(candidato: tuple, eleitor: tuple) -> bool:
    """Logs como (termo_da_ultima_entrada, indice_da_ultima_entrada).
    True se o log do candidato é PELO MENOS tão atualizado quanto o do eleitor:
    termo maior; ou mesmo termo e índice maior ou igual."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def apurar_eleicao(pedidos: list, eleitores: dict, n_total: int):
    """pedidos = [(candidato, log_do_candidato)] na ORDEM em que chegam aos eleitores (mesmo termo).
    eleitores = {nome: log}. Todos os candidatos se candidataram ao mesmo tempo: cada um já votou
    em SI MESMO. Os demais eleitores votam no PRIMEIRO pedido que chega cujo log passa em log_ok, e só
    uma vez (percorra os eleitores em ordem alfabética). Retorne {"votos": {candidato: n},
    "lider": candidato com maioria estrita de n_total, ou None}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
