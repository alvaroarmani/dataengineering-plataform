"""Testes do Exercício 06 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import anomalia_volume  # noqa: E402


def test_anomalia_volume():
    assert anomalia_volume(*([100, 110, 90], 300, 0.5)) == True
    assert anomalia_volume(*([100, 110, 90], 105, 0.5)) == False
