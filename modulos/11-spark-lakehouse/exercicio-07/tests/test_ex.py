"""Testes do Exercício 07 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import arquivos_da_versao  # noqa: E402


def test_arquivos_da_versao():
    assert arquivos_da_versao(*([['a.parquet'], ['a.parquet', 'b.parquet'], ['b.parquet', 'c.parquet']], 0)) == ['a.parquet']
    assert arquivos_da_versao(*([['a.parquet'], ['a.parquet', 'b.parquet'], ['b.parquet', 'c.parquet']], 2)) == ['b.parquet', 'c.parquet']
