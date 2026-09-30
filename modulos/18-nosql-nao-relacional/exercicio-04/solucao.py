"""Exercício 04 (M18) — Chave de partição: medir o hotspot antes de ir para produção.

Rode `pytest -q`.

Num banco wide-column (Cassandra) ou key-value particionado (DynamoDB), o nó de cada linha é
decidido por hash(partition key). Aqui você vai simular isso e MEDIR a distribuição.

Use SEMPRE este hash (estável entre execuções — o hash() do Python não é):
    zlib.crc32("|".join(str(v) for v in valores).encode("utf-8")) % n
"""
import zlib  # noqa: F401  (você vai precisar)


def particao(valores: tuple, n: int) -> int:
    """Partição (0..n-1) de uma chave cujos valores são `valores`, com o hash acima."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def distribuicao(registros: list, chave: list, n: int) -> list:
    """Lista com n contagens: quantos registros caem em cada partição usando as colunas `chave`
    (na ordem dada) como partition key."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fator_skew(contagens: list) -> float:
    """max(contagens) / média(contagens), com 2 casas. 1.0 = perfeitamente uniforme.
    Lista vazia ou total zero -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def escolher_chave(registros: list, candidatas: list, n: int, campos_da_consulta: list) -> tuple:
    """Escolha a melhor partition key entre as `candidatas` (listas de colunas).

    - Só é ELEGÍVEL a chave cujas colunas a consulta conhece (todas estão em `campos_da_consulta`):
      sem conhecer a chave inteira, o banco não sabe em que partição procurar.
    - Entre as elegíveis, vence o menor fator_skew; empate -> menos colunas; depois ordem alfabética.
    - Retorne (tupla_da_chave, fator_skew). Nenhuma elegível -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
