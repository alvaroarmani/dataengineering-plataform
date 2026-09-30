import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import arquivos_gravados, planejar_particoes  # noqa: E402


def test_tabela_de_50gb_em_32_cores():
    assert planejar_particoes(50_000, 32) == {"particoes": 416, "mb_por_particao": 120.2, "ondas": 13}


def test_tabela_pequena_ainda_usa_todos_os_cores():
    assert planejar_particoes(300, 16) == {"particoes": 16, "mb_por_particao": 18.8, "ondas": 1}


def test_alvo_maior_menos_particoes():
    assert planejar_particoes(50_000, 32, alvo_mb=256)["particoes"] == 224


def test_arquivos_pequenos():
    # 200 tarefas, cada uma com linhas de todas as 30 datas do mês (dados embaralhados)
    tarefas = [set(range(1, 31))] * 200
    assert arquivos_gravados(tarefas, repartition_por_data=False) == 6_000
    assert arquivos_gravados(tarefas, repartition_por_data=True) == 30


def test_dados_ja_organizados_e_vazio():
    assert arquivos_gravados([{1}, {2}, {3}], repartition_por_data=False) == 3
    assert arquivos_gravados([], True) == 0
    with pytest.raises(ValueError):
        planejar_particoes(100, 0)
