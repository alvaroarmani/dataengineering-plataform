"""Testes do Exercício 04 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import dedup  # noqa: E402


def test_dedup_mais_recente():
    linhas = [
        (1, 100, "2026-08-10"),
        (2, 200, "2026-08-10"),
        (3, 300, "2026-08-11"),
        (1, 150, "2026-08-12"),
    ]
    assert dedup(linhas) == [(1, 150), (2, 200), (3, 300)]


def test_dedup_sem_duplicatas():
    linhas = [(5, 50, "2026-01-01"), (6, 60, "2026-01-02")]
    assert dedup(linhas) == [(5, 50), (6, 60)]


def test_dedup_vazio():
    assert dedup([]) == []


def test_chegada_fora_de_ordem():
    # a reentrega antiga chegou DEPOIS da nova: quem manda é carregado_em, não a posição
    linhas = [(1, 150, "2026-08-12T09:00:00"), (1, 100, "2026-08-10T23:59:59")]
    assert dedup(linhas) == [(1, 150)]


def test_empate_de_carregado_em_vence_a_ultima_da_lista():
    linhas = [(7, "a", "2026-08-12T10:00:00"), (7, "b", "2026-08-12T10:00:00")]
    assert dedup(linhas) == [(7, "b")]


def test_exclusao_logica_remove_o_id():
    linhas = [(1, 100, "2026-08-10"), (2, 200, "2026-08-10"), (1, None, "2026-08-11")]
    assert dedup(linhas) == [(2, 200)]


def test_exclusao_seguida_de_recriacao():
    linhas = [(1, None, "2026-08-11"), (1, 100, "2026-08-10"), (1, 120, "2026-08-12")]
    assert dedup(linhas) == [(1, 120)]


def test_nao_muta_a_entrada():
    linhas = [(2, 20, "2026-08-11"), (1, 10, "2026-08-10")]
    dedup(linhas)
    assert linhas == [(2, 20, "2026-08-11"), (1, 10, "2026-08-10")]
