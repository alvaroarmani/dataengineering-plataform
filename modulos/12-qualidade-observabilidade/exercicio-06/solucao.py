"""Exercício 06 (M12) — Anomalia de volume com z-score.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

from statistics import fmean, pstdev


def avaliar_volume(historico: list, atual: int, z_max: float = 3.0, min_historico: int = 7) -> dict:
    """Retorne {"anomalia": bool, "z": z com 2 casas ou None, "direcao": "queda"|"alta"|None}.

    - Histórico com menos de `min_historico` pontos -> ValueError (não dá para julgar).
    - z = (atual - média) / desvio-padrão POPULACIONAL (statistics.pstdev).
    - anomalia = |z| > z_max; "direcao" só é preenchida quando há anomalia.
    - Desvio-padrão zero (histórico constante): z = None e anomalia = (atual != média).
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
