"""Testes do Exercicio 03 (M1). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ordena_ciclo_vida  # noqa: E402


def test_ordena_ciclo_vida():
    assert ordena_ciclo_vida(*(['transformacao', 'geracao', 'ingestao'],)) == ['geracao', 'ingestao', 'transformacao']
    assert ordena_ciclo_vida(*(['disponibilizacao', 'armazenamento'],)) == ['armazenamento', 'disponibilizacao']
