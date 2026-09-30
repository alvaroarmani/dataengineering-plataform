"""Testes do Exercício 01 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import custo_container, custo_serverless, ponto_de_equilibrio, recomendar  # noqa: E402


def test_custo_serverless_com_cota_gratuita():
    assert custo_serverless(500_000, 200, 0.5) == 0.0          # tudo dentro da cota
    assert custo_serverless(3_000_000, 200, 0.5) == 0.4        # só as requisições passam da cota
    assert custo_serverless(20_000_000, 200, 0.5) == 30.47     # requisições + GB-s


def test_custo_container_ligado_o_mes_todo():
    assert custo_container(0.5, 1) == 18.02
    assert custo_container(0.5, 1, replicas=2) == 36.04         # alta disponibilidade dobra o custo
    assert custo_container(1, 2) == 36.04


def test_recomendar_trafego_baixo_e_alto():
    assert recomendar(3_000_000, 200, 0.5, 0.5, 1) == {
        "escolha": "serverless", "serverless": 0.4, "container": 18.02, "economia_pct": 97.8}
    assert recomendar(50_000_000, 200, 0.5, 0.5, 1) == {
        "escolha": "container", "serverless": 86.47, "container": 18.02, "economia_pct": 79.2}


def test_recomendar_sem_trafego():
    r = recomendar(0, 200, 0.5, 0.5, 1)
    assert r["escolha"] == "serverless" and r["economia_pct"] == 100.0


def test_ponto_de_equilibrio_e_a_fronteira_exata():
    pe = ponto_de_equilibrio(200, 0.5, 0.5, 1)
    assert pe == 13_334_805                                     # ~5 requisições por segundo
    assert custo_serverless(pe - 1, 200, 0.5) <= custo_container(0.5, 1) < custo_serverless(pe, 200, 0.5)


@pytest.mark.parametrize("args, esperado", [
    ((1000, 1, 0.5, 1), 1_475_789),       # função lenta e grande: o container compensa cedo
    ((200, 0.5, 0.5, 1, 2), 22_988_359),  # 2 réplicas: o serverless aguenta mais tráfego
    ((50, 0.125, 0.5, 1), 81_835_605),    # função rápida e leve: serverless até ~31 req/s
])
def test_ponto_de_equilibrio_depende_do_perfil(args, esperado):
    assert ponto_de_equilibrio(*args) == esperado


@pytest.mark.parametrize("chamada", [
    lambda: custo_serverless(-1, 200, 0.5),
    lambda: custo_serverless(10, -5, 0.5),
    lambda: custo_container(0, 1),
    lambda: custo_container(0.5, 1, replicas=0),
])
def test_entradas_invalidas(chamada):
    with pytest.raises(ValueError):
        chamada()
