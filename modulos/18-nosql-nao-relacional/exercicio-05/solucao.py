"""Exercício 05 (M18) — Série temporal: rollup, reagregação e retenção (como um TSDB).

Rode `pytest -q`.

Pontos são tuplas (timestamp_seg, valor). Um "rollup" é um dict ORDENADO por início do bucket:
    {inicio: {"n": qtd_de_pontos, "min": ..., "max": ..., "media": média com 2 casas}}
"""


def rollup(pontos: list, bucket_seg: int) -> dict:
    """Agregue os pontos em buckets fixos de bucket_seg segundos (início = ts // bucket * bucket).
    Chaves em ordem crescente; buckets sem pontos NÃO aparecem. bucket_seg <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def reagregar(rollups: dict, bucket_seg: int) -> dict:
    """Transforme um rollup FINO (ex.: por minuto) num mais GROSSO (ex.: por hora) SEM os pontos
    brutos — é assim que o TSDB desce de resolução depois de apagar o dado original.
    O resultado deve ser IGUAL (a menos do arredondamento da média) ao rollup direto dos pontos.
    bucket_seg <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def aplicar_retencao(pontos: list, agora: int, janela_bruta_seg: int, bucket_seg: int) -> tuple:
    """Política de retenção: pontos com ts >= agora - janela_bruta_seg ficam BRUTOS (lista ordenada
    por ts); os mais antigos só sobrevivem como rollup(…, bucket_seg).
    Retorne (pontos_recentes, rollup_dos_antigos)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
