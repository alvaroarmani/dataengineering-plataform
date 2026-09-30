"""Exercício 10 (M7) — Watermark incremental: a linha perdida no empate e o lookback.

Rode `pytest -q`. Detalhes no enunciado (exercicio-10.md).
"""


def selecionar_incremental(linhas: list, watermark, lookback: int = 0) -> tuple:
    """linhas = dicts com "id" e "updated_at" (inteiros). Selecione as linhas com
    updated_at > watermark - lookback (watermark None = primeira carga: tudo).
    Retorne (selecionadas na ordem de entrada, novo_watermark = maior updated_at entre watermark e as
    selecionadas). lookback < 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def simular_cargas(chegadas: list, lookback: int) -> set:
    """chegadas = lista de lotes; cada lote é a lista de linhas que CHEGARAM à fonte desde a carga anterior.
    A cada carga, a fonte contém tudo o que chegou até ali. Rode selecionar_incremental carga a carga
    (atualizando o watermark) e acumule os ids carregados (um set, como um merge idempotente faria).
    Retorne o conjunto final de ids no destino."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
