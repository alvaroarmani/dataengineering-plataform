"""Exercício 05 (M15) — System design: requisitos em números (estimativa de capacidade).

Rode `pytest -q`.

Numa entrevista de system design, antes de desenhar caixinhas você estima: quantos eventos por
segundo (média e pico)? Quanto disco? Isso decide a arquitetura. Use 1 dia = 86.400 s e
1 TB = 10**12 bytes; 1 GB = 10**9 bytes.
"""


def vazao(eventos_dia: int, fator_pico: float = 3.0) -> dict:
    """{"media_s": eventos/s em média, "pico_s": média * fator_pico}, ambos com 1 casa.
    eventos_dia < 0 ou fator_pico < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def armazenamento_tb(eventos_dia, bytes_evento, retencao_dias, replicas=1, compressao=1.0) -> float:
    """TB ocupados: eventos_dia * bytes_evento * retencao_dias * replicas / compressao, em TB, 3 casas.
    Valores negativos, replicas < 1 ou compressao <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def proposta(req: dict) -> dict:
    """req traz OBRIGATORIAMENTE eventos_dia, bytes_evento, latencia_seg, retencao_dias
    (e opcionalmente fator_pico=3.0, replicas=1, compressao=1.0). Falta obrigatório -> ValueError.

    Retorne:
      "processamento": "batch" se latencia_seg >= 3600; "micro-batch" se >= 60; senão "streaming"
      "motor":         "spark" se o volume BRUTO diário (eventos_dia * bytes_evento) passa de 500 GB;
                       senão "sql-warehouse"  (a solução mais simples que atende)
      "pico_s":        o pico de vazao(...)
      "armazenamento_tb": armazenamento_tb(...)
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
