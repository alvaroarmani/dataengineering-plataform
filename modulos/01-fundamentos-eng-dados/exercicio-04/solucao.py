"""Exercício 04 (M1) — Qual arquitetura de dados? (decisão a partir de REQUISITOS).

Você recebe os requisitos de um projeto e devolve a arquitetura recomendada **com os motivos**.
Rode `pytest -q`.

Um requisito é um dict:
    {"formatos": ["tabular", "json", ...],       # o que chega das fontes
     "consumidores": ["bi", "ml", ...],          # quem usa o dado
     "precisa_acid": False}                      # opcional (padrão False)
"""

FORMATOS = {"tabular", "json", "log", "imagem", "audio"}
CONSUMIDORES = {"bi", "sql_adhoc", "ml", "arquivamento"}


def recomendar_arquitetura(req: dict) -> dict:
    """Retorne {"arquitetura": ..., "motivos": [...]} com os motivos em ordem alfabética.

    Motivos (inclua TODOS os que se aplicam):
      - "dados_nao_estruturados": algum formato diferente de "tabular"
      - "consumo_ml":            "ml" entre os consumidores
      - "arquivamento_barato":   "arquivamento" entre os consumidores
      - "bi_com_esquema":        "bi" ou "sql_adhoc" entre os consumidores
      - "transacoes_acid":       precisa_acid verdadeiro
    Os três primeiros pedem um LAKE; os dois últimos pedem garantias de WAREHOUSE.
      - só lake → "data-lake";  só warehouse → "data-warehouse";  os dois → "lakehouse".

    Levante ValueError se: "formatos" ou "consumidores" estiver vazio/ausente, ou se aparecer
    formato/consumidor fora de FORMATOS/CONSUMIDORES.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
