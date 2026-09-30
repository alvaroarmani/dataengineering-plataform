"""Exercício 05 (M17) — Janelas por tempo de evento com WATERMARK (atrasados e completude).

Rode `pytest -q`.

Os eventos chegam na ORDEM DA LISTA (tempo de processamento), mas cada um carrega o seu `ts`
(tempo de evento, em segundos): {"id": "a", "ts": 58, "valor": 4}.
"""


def janela_tumbling(event_ts: int, tamanho_seg: int) -> int:
    """Início da janela fixa (tumbling) que contém event_ts. tamanho_seg <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def processar_stream(eventos: list, tamanho_seg: int, atraso_permitido_seg: int) -> dict:
    """Simule um motor de streaming que soma `valor` por janela tumbling de tempo de evento.

    Para cada evento, NA ORDEM DE CHEGADA:
      1. Se a janela dele já foi FECHADA (inicio + tamanho <= watermark atual), o evento é ATRASADO:
         registre o id em "atrasados" e ignore-o (não altera nada, nem o watermark).
      2. Senão, some o valor na janela e atualize:
             watermark = max(watermark, ts - atraso_permitido_seg)
         (antes do primeiro evento aceito, não há watermark).
      3. Feche e EMITA, em ordem de início, toda janela aberta com inicio + tamanho <= watermark.
    No fim do stream, emita as janelas ainda abertas, em ordem de início.

    Retorne {"janelas": [(inicio, soma), ...] na ORDEM EM QUE FORAM EMITIDAS,
             "atrasados": [ids na ordem de chegada]}.
    atraso_permitido_seg < 0 -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
