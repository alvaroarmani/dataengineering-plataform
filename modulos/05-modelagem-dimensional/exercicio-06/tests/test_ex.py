"""Testes do Exercício 06 (M5). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE stg_produto(codigo VARCHAR, categoria VARCHAR)')
    c.executemany('INSERT INTO stg_produto VALUES (?,?)', [('P-30', 'casa'), ('P-10', 'eletronicos'), ('P-20', 'livros')])
    c.execute('CREATE TABLE stg_venda(venda_id INT, codigo_produto VARCHAR, valor INT)')
    c.executemany('INSERT INTO stg_venda VALUES (?,?,?)', [(1, 'P-10', 100), (2, 'P-30', 50), (3, 'P-10', 120)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [(1, 'P-10', 'eletronicos'), (2, 'P-20', 'livros'), (3, 'P-30', 'casa')]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [(1, 1, 100), (2, 3, 50), (3, 1, 120)]
