"""Exercício 02 (M18) — Um pipeline de agregação estilo MongoDB.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""


def agregar(docs: list, pipeline: list) -> list:
    """Execute os estágios em ordem, sem alterar `docs`. Cada estágio é um dict de UMA chave:
      {"$match": {caminho: valor}}   mantém docs em que TODOS os caminhos são iguais ao valor
                                     (caminho com ponto acessa campo aninhado; ausente = None)
      {"$unwind": "campo"}          um doc por elemento do array (o campo passa a ser o elemento);
                                     doc sem o campo ou com array vazio SOME
      {"$group": {"_id": "$caminho", saida: {"$sum": 1 | "$caminho"}, saida2: {"$avg": "$caminho"}}}
                                     um doc por valor distinto (na ordem em que aparece); $avg com 2 casas
      {"$sort": {caminho: 1 | -1, ...}}  ordena por várias chaves (a primeira manda)
    Estágio desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
