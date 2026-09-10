"""Exercicio 09 (M8) - Aplicar changelog CDC (complexo). Implemente e rode `pytest -q`."""


def aplicar_cdc(estado, eventos):
    """Materialize a tabela-espelho aplicando um changelog de CDC. estado = {chave: valor} atual; eventos = lista de dicts {op, chave, valor} com op em 'I'/'U'/'D', aplicados EM ORDEM. I e U fazem upsert; D remove. Retorne o estado final (dict)."""
    # SEU CODIGO AQUI
    raise NotImplementedError
