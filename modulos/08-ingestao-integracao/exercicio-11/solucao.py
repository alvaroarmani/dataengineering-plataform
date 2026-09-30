"""Exercício 11 (M08) — Ingerindo a PTAX REAL do Banco Central (mini-caso).

Dados: datasets/amostras/ptax_2024_01.json — resposta real (sem edição) da API OData PTAX do Banco
Central para o dólar em jan/2024. Rode `pytest -q`.

Formato do payload (contrato da API):
    {"@odata.context": "...",
     "value": [{"cotacaoCompra": 4.891, "cotacaoVenda": 4.8916,
                "dataHoraCotacao": "2024-01-02 13:05:50.319"}, ...]}
Um "registro" normalizado é um dict: {"data": "AAAA-MM-DD", "compra": float, "venda": float}.
"""


def normalizar_ptax(payload: dict) -> list:
    """Transforme o payload em lista de registros normalizados, ORDENADA por data.
    Se o payload não tiver a chave 'value' (contrato quebrado), levante ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def upsert_por_data(destino: list, novos: list) -> list:
    """Integre `novos` em `destino` por data, de forma IDEMPOTENTE: data nova entra, data existente
    é substituída pelo registro novo. Retorne a lista resultante ordenada por data."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def dias_sem_cotacao(registros: list, inicio: str, fim: str, feriados: list) -> list:
    """Checagem de COMPLETUDE: retorne (ordenados) os dias úteis entre inicio e fim (inclusive,
    'AAAA-MM-DD') que NÃO têm registro. Dia útil = segunda a sexta que não está em `feriados`."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def maior_variacao_diaria(registros: list):
    """Entre dias CONSECUTIVOS da lista (já ordenada), ache a maior variação percentual da cotação
    de venda em valor absoluto. Retorne (data_do_dia_da_variacao, variacao_pct) com a variação
    arredondada a 4 casas (negativa se o dólar caiu). Menos de 2 registros → None."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
