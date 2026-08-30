"""Testes do Exercício 02 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import enviados_ao_contexto  # noqa: E402


def test_enviados_ao_contexto():
    assert enviados_ao_contexto(*(['app.py', 'node_modules/x', '.env', 'src/a.py'], ['node_modules/', '.env'])) == ['app.py', 'src/a.py']
