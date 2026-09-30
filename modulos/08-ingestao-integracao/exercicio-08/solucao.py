"""Exercício 08 (M8) — Consumo por offset: lotes, retenção e auto.offset.reset.

Rode `pytest -q`. Detalhes no enunciado (exercicio-08.md).
"""


def poll(log: list, inicio_log: int, offset: int, max_msgs: int = 500, reset: str = "earliest") -> dict:
    """log = mensagens disponíveis; a primeira tem offset `inicio_log` (as anteriores foram apagadas pela
    retenção). offset = próximo offset que o consumidor quer ler. fim = inicio_log + len(log).
      - offset > fim -> ValueError (offset inválido).
      - offset < inicio_log (apagado): reset "earliest" -> lê a partir de inicio_log;
        "latest" -> vai para o fim (nada lido); "none" -> ValueError. As mensagens puladas entre o offset
        pedido e o ponto de leitura contam em "perdidas".
      - leia no máximo max_msgs mensagens a partir do ponto de leitura.
    Retorne {"mensagens": [...], "proximo_offset": n, "perdidas": n}. max_msgs < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
