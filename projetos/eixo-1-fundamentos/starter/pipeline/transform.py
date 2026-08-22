"""Etapa 2 — Transformação: limpar e enriquecer os pedidos.

Implemente as três funções abaixo (puras: recebem um DataFrame, retornam um novo).
Rode `pytest -q` na pasta do starter até tudo passar.
"""
import pandas as pd


def padronizar_estado(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna uma cópia com a coluna 'estado' em MAIÚSCULAS (ex.: 'sp' -> 'SP')."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna uma cópia com 'valor' convertido para número e as linhas inválidas removidas.

    Dica: pd.to_numeric(..., errors='coerce') transforma o que não é número em NaN;
    depois use dropna(subset=['valor']).
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def adicionar_receita(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna uma cópia com uma nova coluna 'receita' = valor * quantidade."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
