"""Exercício 01 (M11) — Lazy evaluation: quantas vezes a fonte é lida (e o cache).

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""


TRANSFORMACOES = {"filter", "select", "withColumn", "join", "groupBy", "orderBy", "distinct"}
ACOES = {"count", "show", "collect", "write", "first"}


def simular(ops: list) -> dict:
    """ops = sequência de operações num MESMO DataFrame (cada uma se aplica ao resultado da anterior):
    transformações (TRANSFORMACOES), ações (ACOES), "cache" e "unpersist".
    Regras:
      - transformação: só entra no plano (nenhuma leitura);
      - ação: se houver cache materializado válido, reaproveita (0 leituras da fonte); senão, lê a fonte
        (1 leitura) — e, se houver um cache pendente, ele é materializado nessa ação;
      - "cache": marca como pendente; "unpersist": descarta o cache (materializado ou pendente);
      - uma transformação DEPOIS do cache não invalida o cache (o Spark reaproveita a parte cacheada).
    Retorne {"acoes": n, "leituras_da_fonte": n}. Operação desconhecida -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
