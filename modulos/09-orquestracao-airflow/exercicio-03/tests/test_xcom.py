"""Testes do Exercício 03 (M9). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import rodar_tasks  # noqa: E402


def test_passa_valores_entre_tasks():
    tasks = [
        ("extrair", lambda x: [1, 2, 3]),
        ("somar", lambda x: sum(x["extrair"])),
        ("dobrar", lambda x: x["somar"] * 2),
    ]
    assert rodar_tasks(tasks) == {"extrair": [1, 2, 3], "somar": 6, "dobrar": 12}


def test_uma_task():
    assert rodar_tasks([("t", lambda x: 42)]) == {"t": 42}


def test_ordem_importa():
    # 'b' usa o resultado de 'a' -> 'a' precisa rodar antes
    tasks = [("a", lambda x: 10), ("b", lambda x: x["a"] + 5)]
    assert rodar_tasks(tasks) == {"a": 10, "b": 15}
