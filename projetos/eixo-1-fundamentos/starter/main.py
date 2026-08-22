"""Orquestra o pipeline: ingestão -> transformação -> carga -> análise.

Rode: python main.py
(Só funciona depois que você implementar transform.py e load.py.)
"""
import duckdb

from pipeline.ingest import ler_pedidos
from pipeline.load import carregar
from pipeline.transform import adicionar_receita, limpar, padronizar_estado

DB = "pedidos.duckdb"


def rodar():
    df = ler_pedidos()
    print(f"ingeridos: {len(df)} pedidos (brutos)")

    # transformação: compõe os passos (funções puras)
    df = padronizar_estado(df)
    df = limpar(df)
    df = adicionar_receita(df)
    print(f"após limpeza: {len(df)} pedidos válidos")

    carregar(df, DB)

    # análise: receita por estado (exemplo — escreva as demais em consultas.sql)
    con = duckdb.connect(DB)
    print("\nReceita por estado:")
    print(con.execute(
        "SELECT estado, SUM(receita) AS receita FROM pedidos "
        "GROUP BY estado ORDER BY receita DESC"
    ).df().to_string(index=False))
    con.close()


if __name__ == "__main__":
    rodar()
