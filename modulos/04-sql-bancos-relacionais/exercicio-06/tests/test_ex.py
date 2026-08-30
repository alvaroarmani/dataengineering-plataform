"""Testes do Exercício 06 (M4). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
import duckdb, pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B  # noqa: E402

@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute('CREATE TABLE produtos(id INT, nome VARCHAR, categoria VARCHAR, preco INT)')
    c.executemany('INSERT INTO produtos VALUES (?,?,?,?)', [(1, 'tv', 'eletronicos', 300), (2, 'livro', 'livros', 40), (3, 'fone', 'eletronicos', 150), (4, 'mesa', 'casa', 200), (5, 'cabo', 'eletronicos', 20)])
    return c

def test_a(con):
    assert con.execute(CONSULTA_A).fetchall() == [('tv', 300), ('fone', 150)]

def test_b(con):
    assert con.execute(CONSULTA_B).fetchall() == [('casa', 200.0), ('eletronicos', 156.66666666666666), ('livros', 40.0)]
