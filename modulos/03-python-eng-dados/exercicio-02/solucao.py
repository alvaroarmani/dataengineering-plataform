"""Exercício 02 (M3) — Um Pipeline de transformações.

Implemente a classe `Pipeline` e rode `pytest -q` nesta pasta até tudo passar.
"""


class Pipeline:
    """Encadeia funções de transformação e as aplica em ordem.

    - Pipeline(passos=None): guarda a lista de funções (vazia se None).
    - adicionar(f): anexa f e retorna self (permite encadear).
    - rodar(dados): aplica os passos em ordem e retorna o resultado.
    """

    def __init__(self, passos=None):
        # SEU CÓDIGO AQUI
        raise NotImplementedError

    def adicionar(self, f):
        # SEU CÓDIGO AQUI
        raise NotImplementedError

    def rodar(self, dados):
        # SEU CÓDIGO AQUI
        raise NotImplementedError
