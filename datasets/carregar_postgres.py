#!/usr/bin/env python3
"""Carrega um dataset (CSV) no Postgres da bancada, usando COPY (rápido).

Uso (com a bancada de pé: cd ambiente && docker compose up -d):
    pip install psycopg2-binary pyyaml
    python datasets/carregar_postgres.py olist

Cria um schema `raw` e uma tabela por arquivo CSV (nome = arquivo sem extensão).
Idempotente: recria as tabelas (DROP + CREATE a partir do cabeçalho, tudo TEXT).
Lê as credenciais do Postgres das variáveis do .env (POSTGRES_HOST, etc.).
"""
import csv
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "datasets" / "data"


def conectar():
    import psycopg2

    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        user=os.environ.get("POSTGRES_USER", "curso"),
        password=os.environ.get("POSTGRES_PASSWORD", "curso"),
        dbname=os.environ.get("POSTGRES_DB", "curso"),
    )


def carregar_csv(cur, caminho: Path, schema="raw"):
    tabela = caminho.stem
    with caminho.open(encoding="utf-8", newline="") as f:
        cabecalho = next(csv.reader(f))
    cols = ", ".join(f'"{c}" TEXT' for c in cabecalho)
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    cur.execute(f'DROP TABLE IF EXISTS {schema}."{tabela}"')
    cur.execute(f'CREATE TABLE {schema}."{tabela}" ({cols})')
    with caminho.open(encoding="utf-8") as f:
        cur.copy_expert(
            f'COPY {schema}."{tabela}" FROM STDIN WITH (FORMAT csv, HEADER true)', f
        )
    print(f"  carregado {schema}.{tabela}")


def main(argv):
    import yaml

    if not argv:
        print("uso: python datasets/carregar_postgres.py <nome_do_dataset>")
        return
    nome = argv[0]
    manifesto = yaml.safe_load((RAIZ / "datasets" / "manifest.yaml").read_text(encoding="utf-8"))
    spec = manifesto["datasets"].get(nome)
    if not spec:
        print(f"dataset desconhecido: {nome}")
        return
    conn = conectar()
    conn.autocommit = True
    cur = conn.cursor()
    print(f"[{nome}] carregando no Postgres (schema raw)...")
    for rel in spec["arquivos"]:
        caminho = DATA / rel
        if not caminho.exists():
            print(f"  faltando: {caminho.relative_to(RAIZ)} — rode datasets/baixar.py primeiro")
            continue
        if caminho.suffix.lower() == ".csv":
            carregar_csv(cur, caminho)
        else:
            print(f"  {caminho.name}: formato {caminho.suffix} não é CSV — use MinIO/Parquet (ver M11)")
    cur.close()
    conn.close()
    print(f"[{nome}] concluído.")


if __name__ == "__main__":
    main(sys.argv[1:])
