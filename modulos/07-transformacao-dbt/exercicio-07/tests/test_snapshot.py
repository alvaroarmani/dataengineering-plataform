"""Testes do Exercício 07 (M7). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import detectar_mudancas, detectar_novos  # noqa: E402

ATUAL = {1: "SP", 2: "RJ", 3: "MG"}
INCOMING = {1: "SP", 2: "Campinas", 3: "MG", 4: "BA"}


def test_mudancas():
    # cliente 2 mudou (RJ -> Campinas); 1 e 3 iguais; 4 é novo (não conta como mudança)
    assert detectar_mudancas(ATUAL, INCOMING) == [2]


def test_novos():
    assert detectar_novos(ATUAL, INCOMING) == [4]


def test_sem_mudancas_quando_igual():
    assert detectar_mudancas(ATUAL, ATUAL) == []
    assert detectar_novos(ATUAL, ATUAL) == []
