"""Projeto Integrador do Eixo 3 — ELT incremental de uma API (câmbio).

Implemente as três funções (puras). Rode `pytest -q` até tudo passar. Depois, orquestre com
uma DAG Airflow idempotente na bancada (ver README, dags/ e M09).
"""
import pandas as pd


def parse_cotacoes(payload: dict) -> pd.DataFrame:
    """Normaliza a resposta da API para um DataFrame [data, valor], ordenado por data.

    payload["value"] é uma lista de dicts com 'cotacaoCompra' (valor) e 'dataHoraCotacao'
    ('AAAA-MM-DD HH:MM:...'); use só a DATA (os 10 primeiros caracteres).
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def upsert_idempotente(destino: pd.DataFrame, novos: pd.DataFrame) -> pd.DataFrame:
    """Integra `novos` em `destino` por `data`, de forma IDEMPOTENTE.

    Se uma `data` já existe no destino, o valor de `novos` prevalece (overwrite). O resultado
    tem 1 linha por data, ordenado por data. Rodar de novo com os mesmos `novos` não muda nada.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def checar_qualidade(df: pd.DataFrame) -> list:
    """Portão de qualidade: retorna a lista ORDENADA de problemas encontrados, entre:
    'data_duplicada' (datas repetidas), 'valor_negativo' (valor < 0), 'valor_nulo' (valor ausente).
    Sem problemas, retorna [].
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
