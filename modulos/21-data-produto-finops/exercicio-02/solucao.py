"""Exercício 02 (M21) — Showback: quem gasta o quê.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


TIB = 2 ** 40


def ratear_custos(consultas: list, preco_por_tib: float) -> dict:
    """consultas = [{"id", "time", "bytes"}]. Time None ou "" vai para o balde "sem_dono".
    Retorne {time: {"custo": 2 casas, "pct": % do total com 1 casa}} com os times em ordem de
    custo decrescente (empate: nome). Sem consultas -> {}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def maiores_ofensores(consultas: list, preco_por_tib: float, n: int = 3) -> list:
    """As n consultas mais caras: [(id, time_ou_sem_dono, custo com 2 casas)], custo desc, id asc."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
