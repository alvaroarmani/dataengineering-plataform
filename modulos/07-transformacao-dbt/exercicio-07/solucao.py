"""Exercício 07 (M7) — A lógica de um snapshot (SCD2 'check strategy'), em Python.

Um snapshot detecta o que MUDOU entre o estado atual e o que chegou, para versionar.
Implemente as duas detecções e rode `pytest -q`.

Entradas: dicts {chave: valor_do_atributo} (ex.: {cliente_id: cidade}).
"""


def detectar_mudancas(atual, incoming):
    """Chaves presentes NOS DOIS cujo atributo MUDOU (precisam de nova versão SCD2).
    Retorne a lista ORDENADA dessas chaves."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def detectar_novos(atual, incoming):
    """Chaves que existem em `incoming` mas NÃO em `atual` (entidades novas).
    Retorne a lista ORDENADA dessas chaves."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
