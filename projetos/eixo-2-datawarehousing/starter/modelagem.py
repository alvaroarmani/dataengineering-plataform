"""Projeto Integrador do Eixo 2 — modelagem dimensional (star schema).

Implemente as três funções (puras: recebem DataFrame(s), retornam um novo DataFrame).
Rode `pytest -q` na pasta do starter até tudo passar. Depois, faça a versão em **dbt**
(pasta dbt/) sobre a bancada Postgres — ver README e M07.
"""
import pandas as pd


def construir_dim_produto(raw_produtos: pd.DataFrame) -> pd.DataFrame:
    """Dimensão produto com CHAVE SUBSTITUTA (surrogate key).

    Ordene por `produto_id`, adicione `produto_sk` = 1, 2, 3, ... e retorne as colunas
    [produto_sk, produto_id, nome, categoria].
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def construir_fct_vendas(raw_pedidos: pd.DataFrame, dim_produto: pd.DataFrame) -> pd.DataFrame:
    """Fato de vendas (grão: 1 linha por pedido).

    Junte os pedidos à dim_produto pela chave natural `produto_id` para trazer a `produto_sk`,
    calcule `receita = valor * quantidade`, e retorne [pedido_id, produto_sk, cliente_id,
    quantidade, receita] ordenado por `pedido_id`.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def aplicar_scd2(historico: pd.DataFrame) -> pd.DataFrame:
    """Dimensão SCD Tipo 2 a partir do histórico (colunas: produto_id, categoria, data).

    Para cada produto (ordenado por data), gere uma linha por versão com:
      valido_de = data da versão; valido_ate = data da PRÓXIMA versão (ou '9999-12-31' se for a
      atual); is_current = True só na última versão. Colunas de saída:
      [produto_id, categoria, valido_de, valido_ate, is_current].
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
