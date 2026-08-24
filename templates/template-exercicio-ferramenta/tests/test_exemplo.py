"""Teste do TRACK REAL — grade uma query executada no Postgres da bancada.

Padrão: (1) o teste cria dados de fixture numa tabela temporária; (2) lê a query do
aluno de solucao.sql; (3) executa e confere o resultado. Como a fixture `pg` faz
rollback, o banco não fica sujo entre execuções.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def carregar_sql(nome="solucao.sql"):
    return (RAIZ / nome).read_text(encoding="utf-8")


def test_exemplo(pg):
    cur = pg.cursor()
    # 1) fixture: dados de exemplo numa tabela temporária (some no rollback)
    cur.execute("CREATE TEMP TABLE vendas(estado TEXT, valor NUMERIC)")
    cur.executemany(
        "INSERT INTO vendas VALUES (%s, %s)",
        [("SP", 100), ("RJ", 200), ("SP", 80)],
    )
    # 2) executa a query do aluno
    cur.execute(carregar_sql())
    # 3) confere (ex.: receita por estado, desc)
    assert cur.fetchall() == [("RJ", 200), ("SP", 180)]
