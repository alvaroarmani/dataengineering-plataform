"""Exercício 04 (M9) — Sensor: modo poke x reschedule e o custo de esperar.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def simular_sensor(disponivel_em, intervalo: int, timeout: int, modo: str) -> dict:
    """Tempo em minutos a partir de 0. A condição fica verdadeira no minuto `disponivel_em`
    (None = nunca). O sensor checa nos minutos 0, intervalo, 2*intervalo, ... enquanto o minuto for
    <= timeout. Cada checagem conta como um poke e ocupa o slot por 1 minuto.
      sucesso: a primeira checagem com minuto >= disponivel_em
      minutos_de_slot:
        "poke"       -> do minuto 0 até o fim (a checagem de sucesso, ou o timeout), + 1
        "reschedule" -> 1 por checagem
    Retorne {"sucesso": bool, "pokes": n, "minuto_fim": minuto da última checagem, "minutos_de_slot": n}.
    intervalo < 1 ou modo desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
