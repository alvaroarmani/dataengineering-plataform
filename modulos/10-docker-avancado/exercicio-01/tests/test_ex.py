"""Testes do Exercício 01 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import camadas_reconstruidas  # noqa: E402


def test_camadas_reconstruidas():
    assert camadas_reconstruidas(*(['FROM', 'COPY req', 'RUN pip', 'COPY .', 'CMD'], 2)) == ['RUN pip', 'COPY .', 'CMD']
    assert camadas_reconstruidas(*(['a', 'b'], 0)) == ['a', 'b']
    assert camadas_reconstruidas(*(['a', 'b', 'c'], 3)) == []
