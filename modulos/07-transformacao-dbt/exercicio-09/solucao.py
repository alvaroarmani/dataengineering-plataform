"""Exercicio 09 (M7) - Merge incremental com dado atrasado (complexo). Implemente e rode `pytest -q`."""


def merge_incremental(destino, batch, chave):
    """Estrategia incremental 'merge' com protecao contra dado atrasado. destino e batch = listas de dicts com a `chave`, 'valor' e 'updated_at'. Faca upsert do batch no destino: insira chaves novas e ATUALIZE existentes SOMENTE se o updated_at do batch for >= o do destino (registro atrasado/antigo NAO sobrescreve). Retorne a lista final ordenada por `chave`."""
    # SEU CODIGO AQUI
    raise NotImplementedError
