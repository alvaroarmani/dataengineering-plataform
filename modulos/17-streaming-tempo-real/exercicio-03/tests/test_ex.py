import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import chaves_remapeadas, particao, produzir  # noqa: E402

MSGS = [("cliente-7", "7:login"), ("cliente-11", "11:login"), (None, "ping-1"),
        ("cliente-7", "7:compra"), (None, "ping-2"), ("cliente-11", "11:compra"),
        ("cliente-7", "7:logout"), (None, "ping-3")]


def test_particao_estavel():
    assert particao("cliente-7", 3) == 2
    assert particao("cliente-11", 3) == 0


def test_ordem_por_chave_preservada():
    parts = produzir(MSGS, 3)
    assert [v for v in parts[particao("cliente-7", 3)] if v.startswith("7:")] == ["7:login", "7:compra", "7:logout"]
    assert [v for v in parts[particao("cliente-11", 3)] if v.startswith("11:")] == ["11:login", "11:compra"]


def test_distribuicao_exata():
    assert produzir(MSGS, 3) == {
        0: ["11:login", "ping-1", "11:compra"],
        1: ["ping-2"],
        2: ["7:login", "7:compra", "7:logout", "ping-3"],
    }


def test_particoes_vazias_aparecem():
    assert produzir([("cliente-7", "x")], 4) == {0: ["x"], 1: [], 2: [], 3: []}


def test_aumentar_particoes_remapeia_chaves():
    chaves = [f"cliente-{i}" for i in range(10)]
    assert chaves_remapeadas(chaves, 3, 3) == []
    assert chaves_remapeadas(chaves, 3, 6) == ["cliente-0", "cliente-1", "cliente-6", "cliente-8", "cliente-9"]
