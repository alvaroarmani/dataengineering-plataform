"""Exercício 08 (M3) — Sessionização: início, fim e duração de cada sessão.

Rode `pytest -q`. Detalhes no enunciado (exercicio-08.md).
"""


def sessionizar(eventos: list, gap_max: float) -> dict:
    """eventos = [(usuario, timestamp)] em QUALQUER ordem, possivelmente com (usuario, timestamp) repetido.
    Por usuário: descarte duplicatas exatas, ordene e quebre uma nova sessão quando o intervalo para o
    evento anterior for MAIOR que gap_max (igual ainda é a mesma sessão).
    Retorne {usuario: [(inicio, fim, n_eventos), ...]} com os usuários em ordem alfabética.
    gap_max <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def resumo_por_usuario(sessoes: dict) -> dict:
    """{usuario: {"sessoes": qtd, "eventos": total, "duracao_media": média de (fim - inicio), 1 casa}}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
