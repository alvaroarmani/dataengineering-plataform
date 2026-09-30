"""Testes do Exercício 05 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import janela_tumbling, processar_stream  # noqa: E402

# Cliques de um app; alguns chegam fora de ordem (celular sem rede reenviando depois).
EVENTOS = [
    {"id": "a", "ts": 5, "valor": 1},
    {"id": "b", "ts": 62, "valor": 2},
    {"id": "c", "ts": 58, "valor": 4},     # 4 s atrasado
    {"id": "d", "ts": 75, "valor": 1},
    {"id": "e", "ts": 50, "valor": 8},     # 25 s atrasado
    {"id": "f", "ts": 130, "valor": 3},
    {"id": "g", "ts": 119, "valor": 5},    # 11 s atrasado
    {"id": "h", "ts": 121, "valor": 1},
]


@pytest.mark.parametrize("ts, tam, inicio", [(659, 60, 600), (600, 60, 600), (599, 60, 540), (0, 60, 0), (125, 300, 0)])
def test_janela_tumbling(ts, tam, inicio):
    assert janela_tumbling(ts, tam) == inicio


def test_sem_tolerancia_perde_todo_atrasado():
    assert processar_stream(EVENTOS, 60, 0) == {
        "janelas": [(0, 1), (60, 3), (120, 4)], "atrasados": ["c", "e", "g"]}


def test_tolerancia_de_10s_recupera_so_o_pequeno_atraso():
    assert processar_stream(EVENTOS, 60, 10) == {
        "janelas": [(0, 5), (60, 3), (120, 4)], "atrasados": ["e", "g"]}


def test_tolerancia_de_30s_fica_completo():
    r = processar_stream(EVENTOS, 60, 30)
    assert r == {"janelas": [(0, 13), (60, 8), (120, 4)], "atrasados": []}
    assert sum(s for _, s in r["janelas"]) == sum(e["valor"] for e in EVENTOS)   # nada se perdeu


def test_janela_so_fecha_quando_o_watermark_passa():
    # só 1 evento: nenhuma janela fecha durante o stream; tudo sai no flush final
    assert processar_stream([{"id": "x", "ts": 10, "valor": 7}], 60, 0) == {"janelas": [(0, 7)], "atrasados": []}
    # evento em ts=60 com atraso 0 fecha exatamente a janela [0, 60)
    r = processar_stream([{"id": "x", "ts": 10, "valor": 7}, {"id": "y", "ts": 60, "valor": 1},
                          {"id": "z", "ts": 59, "valor": 100}], 60, 0)
    assert r == {"janelas": [(0, 7), (60, 1)], "atrasados": ["z"]}


def test_atrasado_nao_move_o_watermark():
    # "late" com ts antigo não pode "reabrir" nada nem mudar o que vem depois
    r = processar_stream([{"id": "a", "ts": 100, "valor": 1}, {"id": "old", "ts": 1, "valor": 9},
                          {"id": "b", "ts": 110, "valor": 1}], 60, 0)
    assert r == {"janelas": [(60, 2)], "atrasados": ["old"]}


def test_stream_vazio_e_argumentos_invalidos():
    assert processar_stream([], 60, 10) == {"janelas": [], "atrasados": []}
    with pytest.raises(ValueError):
        processar_stream(EVENTOS, 60, -1)
    with pytest.raises(ValueError):
        janela_tumbling(10, 0)
