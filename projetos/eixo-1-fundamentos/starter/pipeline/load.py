"""Etapa 3 — Carga: gravar o DataFrame limpo numa tabela DuckDB.

Reproduzível: rodar de novo NÃO deve duplicar dados (use CREATE OR REPLACE).
"""
import duckdb
import pandas as pd


def carregar(df: pd.DataFrame, caminho_db: str = "pedidos.duckdb") -> None:
    """Grava `df` na tabela `pedidos` do banco DuckDB em `caminho_db` (sobrescrevendo)."""
    con = duckdb.connect(caminho_db)
    con.register("df_tmp", df)
    # CREATE OR REPLACE garante reprodutibilidade (rodar de novo não duplica)
    con.execute("CREATE OR REPLACE TABLE pedidos AS SELECT * FROM df_tmp")
    con.close()
