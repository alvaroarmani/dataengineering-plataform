"""Testes do Exercício 05 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE fato_vendas(cliente_id INT, produto_id INT, qtd INT, valor INT)')
    c.executemany('INSERT INTO fato_vendas VALUES (?,?,?,?)', [(1, 10, 2, 100), (2, 20, 1, 200), (1, 20, 3, 60), (3, 10, 1, 80), (2, 10, 1, 90)])
    c.execute('CREATE TABLE dim_cliente(cliente_id INT, cidade VARCHAR)')
    c.executemany('INSERT INTO dim_cliente VALUES (?,?)', [(1, 'SP'), (2, 'RJ'), (3, 'MG')])
    c.execute('CREATE TABLE dim_produto(produto_id INT, categoria VARCHAR)')
    c.executemany('INSERT INTO dim_produto VALUES (?,?)', [(10, 'eletronicos'), (20, 'livros')])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('eletronicos', 4), ('livros', 4)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('RJ', 290)]
