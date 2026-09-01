"""Projeto Integrador do Eixo 4 — processamento em escala + qualidade.

Implemente as três funções (puras). Rode `pytest -q` até tudo passar. Depois, reescreva o
`transformar`/`agregar` em **PySpark** gravando Parquet no MinIO (ver README, spark/ e M11).
"""
import pandas as pd


def transformar(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e enriquece as corridas (colunas: pickup, dropoff, passageiros, valor).

    - Calcule `duracao_min` = (dropoff - pickup) em minutos.
    - Derive `data` = data do `pickup` (string 'AAAA-MM-DD').
    - REMOVA corridas inválidas: `duracao_min` <= 0 OU `passageiros` <= 0.
    - Retorne [data, passageiros, valor, duracao_min], índice reiniciado.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def agregar_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega o resultado de `transformar` por `data`:
    `corridas` (contagem), `receita` (soma de valor), `duracao_media` (média de duracao_min).
    Retorne ordenado por `data`, índice reiniciado.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def escrever_parquet(df: pd.DataFrame, caminho: str) -> None:
    """Grave o DataFrame em Parquet (colunar) no `caminho`, sem o índice."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
