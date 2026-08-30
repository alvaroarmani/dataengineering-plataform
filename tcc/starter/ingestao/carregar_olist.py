"""Ingestão: CSV Olist -> schema `raw` do Postgres.

Requisitos do TCC (Etapa 3):
- Reproduzível: rodar do zero recria as tabelas raw.
- Idempotente: rodar de novo NÃO duplica (recria a tabela antes de carregar).
- Sem transformação aqui — raw é fiel à fonte.

TODO: implemente de fato. Esqueleto abaixo usa pandas + SQLAlchemy como sugestão.
"""
from pathlib import Path

DADOS = Path(__file__).parent / "dados"
# TODO: mapeie os CSVs do Olist para nomes de tabela raw.
TABELAS = {
    "olist_orders_dataset.csv": "raw_orders",
    "olist_order_items_dataset.csv": "raw_order_items",
    "olist_customers_dataset.csv": "raw_customers",
    "olist_products_dataset.csv": "raw_products",
    "olist_sellers_dataset.csv": "raw_sellers",
    "olist_order_reviews_dataset.csv": "raw_reviews",
}

DB_URL = "postgresql+psycopg2://dw:dw@localhost:5432/dw"


def carregar() -> None:
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine(DB_URL)
    with engine.begin() as con:
        con.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS raw")
        for arquivo, tabela in TABELAS.items():
            caminho = DADOS / arquivo
            if not caminho.exists():
                print(f"[skip] {arquivo} não encontrado em {DADOS}")
                continue
            df = pd.read_csv(caminho)
            # if_exists='replace' garante idempotência (recria a tabela).
            df.to_sql(tabela, con, schema="raw", if_exists="replace", index=False)
            print(f"[ok] raw.{tabela}: {len(df)} linhas")


if __name__ == "__main__":
    carregar()
